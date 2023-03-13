---
layout: post
title: "Docker Compose: running containers that can talk to each other"
slug: guide-to-docker-compose
date:   2023-03-10 15:00:00 +0000
categories: [containerisation]
tags: [docker, docker-compose]
---

Docker makes setting up and spinning up an application quick and painless by creating an isolated environment on your development machine. However, in most cases, and especially if you're setting up an app that needs data from an external source, you'll need to spin up multiple applications. Technically, a docker container can hold multiple applications, but you wouldn't be taking advantage of the power of docker containers in that case. You can spin up multiple containers, each one containing one application that's part of your setup. However, since docker containers are by default isolated environments, you'll need a way for the containers to communicate with each other. For this, you'll need to set up a single docker network in which to deploy your containers.

A docker network can easily be created via the Docker CLI:
```
docker network create <network-name>
```
You can then build and run containers into the network that you've just created. However, you can end up running a lot of docker commands the more containers you have to spin up, and sometimes it can be easy to forget to configure a new container into the network. This is where **`docker-compose`** comes in handy - you can describe your containers and networking needs through a `docker-compose.yml` file and docker compose takes care of configuring and running your containers for you.

All code in this article are in [this Github repository](https://github.com/shielamms/ds-ml-web-apps/tree/main/docker-compose-demo).

---

## A sample multi-container setup

To demonstrate how to set up a docker network to enable communication between multiple containers, let's take a look at the following app setup. We have a sample app that needs to read and write data from/to a redis cache. The app (in this case, a simple Flask API) is in one container, and the redis instance is in another container. We need to enable communication between the two containers while also allowing users to make API calls to the app.

![DockerComposeDefinition]({{site.baseurl}}/assets/images/docker-compose-definition.png){: width="640" loading="lazy" style="margin-left: 1em; margin-bottom: 1em"}

Both app containers need to be in the same docker network. We expose port 6379 on the redis container so that it can be reached by other apps for data inserts and reads. Then, we expose the API container's port 5001, which will be the entrypoint for API calls from outside of the docker network. 

The redis container is run from an image that's available from docker hub. Meanwhile, the API container is spun up from a custom image that we need to build via a local Dockerfile.


### Building a sample API

Let's write a simple Flask API with three endpoints: one for pinging the API, one for adding data to the redis cache, and one for reading data from the redis cache. We use the `redis` module to establish a connection to a redis host named `redis` (which, at this point, we haven't set up yet) on the default redis port 6379. Note that the redis host name is obtained from an environment variable named `REDIS_HOST`.

`app.py`
```python

import flask
import os
import redis


app = flask.Flask(__name__)

host = os.getenv('REDIS_HOST', 'redis')
client = redis.Redis(host=host, port=6379)


@app.route('/')
def ping():
	return 'Hello!'

@app.route('/cache/<key>/<data>')
def add_data(key, data):
	client.set(key, data)
	return f'Data added into {key}'

@app.route('/retrieve/<key>')
def get_data(key):
	result = client.get(key)
	return result

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

```

Since we've imported `flask` and `redis` in the app, let's go make a `requirements.txt` and list them down and their respective versions. Note that `os` is a native python package, so there's no need to install it.
```
flask==2.2.3
redis==4.5.1
```

We can then create a Dockerfile for this app:

`Dockerfile`
```
FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
COPY app.py .
RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["python"]
CMD ["app.py"]
```

The Dockerfile definition above tells Docker to copy `requirements.txt` and `app.py` into the docker image, then install the app's dependencies specified in `requirements.txt`. The `EXPOSE` directive allows us to open up port `5001` of the container to incoming traffic.

Build the docker image using the above `Dockerfile`. `my-app` below is the name we want to give to the image. Feel free to modify this with your own custom name.
```
docker build -t my-app:latest
```


### Running the redis container

To run a redis container, we can pull the latest redis image from dockerhub, simply by doing a pull:

```
docker pull redis
```

The redis image becomes available in your local docker repository.


### Using docker-compose to define the containers and the network

Now that you have an API image and a redis image, you can now write a `docker-compose.yml` to describe the containers you want to run and how they would communicate with each other through the same network:

`docker-compose.yml`
```
version: "3"

services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    networks:
      - my-network
  my-app:
    depends_on:
      - redis
    image: my-app:latest
    ports:
      - "5000:5000"
    environment:
      REDIS_HOST: "redis"
    networks:
      - my-network

networks:
  my-network:

```

In the above YAML code, the `services` element lists down the containers that you want to run as part of your application. Following our example, we'll be running a redis container and our API container (the API we've arbitrarily called `my-app`). The top-level `networks` element describes the network that we want docker-compose to create for us. In this case, we're creating a network arbitrarily called `my-network`, and leaving the rest of its properties blank to indicate that we just want to set it up with default settings.

Under the `redis` service, the image that docker will run a container from is specified in the `image` property. The port mappings - in this case, the container's port 6379 is mapped to the host's port 6379 - are described in the `ports` property. The network in which to run the container is specified in the `networks` property. Note that we just referred to the name `my-network`, which is defined under the top-level `networks` property.

Under the `my-app` service, the `depends_on` property tells docker-compose to spin up the redis service first before spinning up the `my-app` service. It's a good practice to use this property when spinning up database that an application relies on especially during start-up. We then use the `environment` property to add environment variables to the container - `REDIS_HOST` is needed by the API in order to connect to a redis data source.

Note that both services are described with the same network in their `networks` property - meaning that the containers will be running in the same network.

---

## Let's docker-compose!

We now have our main ingredients for our containerised application: a redis image, an image for our Flask API, and a docker-compose.yml file that describes how to run containers for both images and how they'll communicate with each other. Now we can run docker-compose simply by:

```
docker-compose up
```

You'll then get the following output indicating the order by which the components were created by docker-compose:

```
[+] Running 3/2
 ⠿ Network docker-compose-demo_my-network  Created   0.1s
 ⠿ Container docker-compose-demo-redis-1   Created   0.1s
 ⠿ Container docker-compose-demo-my-app-1  Created   0.1s
```

Below this message will be a standard Flask message telling you that your app is running and listening for traffic on port 5000. Since we've mapped the container's port 5000 with its host's port 5000, we can now do the following API call:

```
curl localhost:5000
```

which should return `Hello!`.

Then we can call another endpoint to add data to the redis cache. For example, the following command will add a key-value pair into redis with `test` as the key and `hello` as the value.

```
curl localhost:5000/cache/test/hello
```

**Output:** `Data added into test`

To retrieve this data from the cache, call the other endpoint:

```
curl localhost:5000/retrieve/test
```

**Output:** `hello`

---

In this primer to docker-compose, we spun up a containerised application composed of a database (redis) and a custom app (Flask API), wherein the custom app is able to reach the database due to them being in the same docker network. The [docker-compose documentation](https://docs.docker.com/compose/compose-file/#volumes-top-level-element) provides more granular details and several more options and elements to configure your docker setup. As your containerised architecture grows, it pays very well to have docker-compose to automate the otherwise mundane and error-prone manual way of running several docker commands.

---