---
layout: post
title: "Docker Compose: running containers that can talk to each other"
slug: guide-to-docker-compose
date:   2023-03-10 15:00:00 +0000
categories: [containerisation]
tags: [docker, docker-compose]
---

Docker makes setting up and spinning up an application quick and painless by creating an isolated environment on your development machine. However, in most cases, and especially if you're setting up an app that needs data from an external source, you'll need to spin up multiple applications. Technically, a docker container can hold multiple applications, but you wouldn't be taking advantage of the power of docker containers in that case. You can spin up multiple containers, each one containing one application that's part of your setup. However, since docker containers are by default isolated environments, you'll need a way for the containers to communicate with each other. For this, you'll need to set up a single docker network in which to deploy your containers.

A docker network easily can be created via the Docker CLI:
```
docker network create <network-name>
```
You can then build and run containers into the network that you've just created. However, you can end up running a lot of docker commands the more containers you have to spin up, and sometimes it can be easy to forget to configure a new container into the network. This is where **`docker-compose`** comes in handy - you can describe your containers and networking needs through a `docker-compose.yml` file and docker compose takes care of configuring and running your containers for you.


## A sample multi-container setup

To demonstrate how to set up a docker network to enable communication between multiple containers, let's take a look at the following app setup. We have a sample app that needs to read and write data from/to a redis cache. The app (in this case, a simple Flask API) is in one container, and the redis instance is in another container. We need to enable communication between the two containers while also allowing users to make API calls to the app.

![DockerComposeDefinition]({{site.baseurl}}/assets/images/docker-compose-definition.png){: width="640" loading="lazy" style="margin-left: 1em; margin-bottom: 1em"}

Both app containers need to be in the same docker network. We expose port 6379 on the redis container so that it can be reached by other apps for data inserts and reads. Then, we expose the API container's port 5001, which will be the entrypoint for API calls from outside of the docker network. 

The redis container is run from an image that's available from docker hub. Meanwhile, the API container is spun up from a custom image that we need to build via a local Dockerfile.


### Running the redis container

To run a redis container, we can pull the latest redis image from dockerhub, simply by doing a pull:

```
docker pull redis
```

The redis image becomes available in your local docker repository, so that you can run a redis container immediately:

```
docker run -r -p 6379:6379 redis
```

### Building and running the API