---
layout: post
title: "Using volumes to share data between docker containers"
slug: guide-to-docker-volumes
date:   2023-03-15 15:00:00 +0000
categories: [containerisation]
tags: [docker, docker-compose]
---

In the [previous docker-compose blog post](http://dev.shielasandoval.com/containerisation/guide-to-docker-compose.html), we explored how docker containers can communicate with each other through a shared network, and then using docker-compose to automatically set up the workflow of running and connecting those containers. In this post, we'll explore how containers can share data (particularly files) with each other without necessarily existing in the same network. This can be achieved by using **docker volumes**, which are specialised Docker-managed directories that can be mounted to multiple containers at the same time. A volume also serves as a persistent file storage for containers, so that when you terminate a container, its data would not be lost and could easily be mounted back to a new container.

Let's take a look at a scenario involving two apps (in separate containers). The first app writes data into a file, while the second app needs to read data from the same file.

All code in this article are in **[this Github repository](https://github.com/shielamms/docker-demos/tree/main/docker-volumes-demo)**.

## Use Case: containers that need to access the same files

Let's say you have an app (which, for simplicity, we'll call `app1`) that's used to write data to a file or several files in a directory. You also have another app (which we'll call `app2`) that needs to read files from this directory and use them for some other downstream task.

![Docker Multicontainer No Sharing]({{site.baseurl}}/assets/images/docker-compose-drawings/docker-compose-no-volume.png){: width="630" loading="lazy" style="margin-bottom: 1em"}

When you spin up a docker container, it will have its own filesystem that's isolated from other containers and from the host itself. This means that merely spinning up containers for `app1` and `app2`, by default, does not mean that they can already access each other's files. There are two ways by which Docker allows multiple containers to share file systems:

1. Through a "bind mount", wherein the host's entire filesystem is mounted into each container. This is not recommended for production systems since anyone who's able to access the host can modify the files that the containers depend on. Anyway, check out [this article from Docker](https://docs.docker.com/storage/bind-mounts/) if you want to learn more about bind mounts, since it will not be covered in this post.

2. Through a **volume**, which is a special storage that's reserved for docker, and therefore can only be managed by docker and accessed by docker containers. By default, this special place is inside the host's filesystem. You can use an external persistent storage (like a bucket or an EFS volume in AWS) as a volume. You can mount volumes to multiple docker containers at the same time, giving each of your containers real-time access to the same data within the volume. You can also control which containers can write data into your volume.

![Docker Multicontainer Shared Volume]({{site.baseurl}}/assets/images/docker-compose-drawings/docker-compose-shared-volume.png){: width="620" loading="lazy" style="margin-bottom: 1em"}

### Creating a volume

You can easily create a volume through the docker CLI:

```
docker volume create <volume-name>
```
where the `<volume-name>` can be any name you want to assign to your volume. Using this command lets docker create a volume within the host's filesystem. Alternatively, you can do this through `docker-compose`, which we'll go over a bit later on in this post.

### Sample apps using the same volume

To demonstrate how volumes work in the context of data sharing between containers, let's spin up two custom app containers - one is an API that has an `/upload` endpoint that allows users to upload a file into a directory named `/data`; while the other is an app that prints out the data from the file in that specified directory.

**`app1`**
`app1` is a Flask API that has two endpoints: `/upload`, which displays a file upload page in your browser; and `/upload-file` which saves the user-uploaded file into the directory named `/data`. Without a volume mounted to this directory in `app1`, it will be just treated as a local directory of its container.

```python
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
VOLUME_PATH = '/data'


@app.route('/upload')
def render_upload_page():
	return render_template('upload.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
	f = request.files['file']
	f.save(os.path.join(VOLUME_PATH, secure_filename(f.filename)))
	return 'File uploaded successfully!'

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

```

As a side note, `secure_filename()` is a type-safe way of uploading files, since it makes sure that the file's name is encoded in ASCII characters before being uploaded into a filesystem. It also checks that the user does not use filenames that are similar to special system filenames.

Then we create a `templates/upload.html` file that contains a form with a file upload button. The form calls the `/upload-file` endpoint at the backend and displays a `File uploaded successfully!` message after the file has been uploaded. 

```html
<html>
	<body>
		<form action="/upload-file" method="POST" enctype="multipart/form-data">
			<input type="file" name="file" />
			<input type="submit" />
		</form>
	</body>
</html>
```

We can then create the `Dockerfile` for `app1`:
```
FROM python:3.10-alpine

WORKDIR /app

RUN mkdir templates
ADD templates/* templates/
ADD *.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["python"]
CMD ["app.py"]

```

Then, build the docker image using the Dockerfile (I used the name `dv-app` arbitrarily):

```
docker build -t dv-app .
```

**`app2`**
Meanwhile, `app2` is meant to read a file named `hello.txt` from the same `/data` directory. Without a volume mounted to this directory in `app2`, then `app2` would just treat the `/data` directory as a local directory that's entirely different from that of `app1`.

```python
import os
import flask

app = flask.Flask(__name__)
VOLUME_PATH = '/data'
TEST_FILENAME = 'hello.txt'

@app.route('/')
def read_file():
	contents = None
	with open(os.path.join(VOLUME_PATH, TEST_FILENAME), 'r') as file:
		contents = file.read()
	return contents

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

```

The `Dockerfile` for `app2` would then be something like the following:

```
FROM python:3.10-alpine

WORKDIR /app
ADD * .

RUN pip install -r requirements.txt

EXPOSE 5002

ENTRYPOINT ["python"]
CMD ["app.py"]

```

Note that we've used port `5001` for `app1`, and port `5002` for `app2`.

Then, we can build the docker image for `app2` accordingly:
```
docker build -t dv-app2 .
```

---

## Using docker-compose to run the containers and mount a volume

Using the Docker CLI, we can create a docker volume, then mount this volume to each of the containers when when running them. This would entail doing the following commands, in order:

```
docker volume create my-shared-volume

# run the first app and mount the created volume
docker run -d -p 5001:5000 --name dv-app1 --mount type=volume,source=my-shared-volume,destination=/data dv-app

# run the second app and mount the created volume
docker run -d -p 5001:5000 --name dv-app2 --mount type=volume,source=my-shared-volume,destination=/data,readonly dv-app2

```

The `docker run` command above uses the `--mount` option to specify that we're mounting a volume (as opposed to a "bind mount" mentioned earlier) into the `/data` directory of the container. Note the extra option `readonly` when running `dv-app2`: this means that we want this container to only have read permissions on the mounted volume.

The same thing can be achieved by **docker-compose**. Below is a simple configuration in `docker-compose.yml`:

```yaml
version: "3"
name: "docker-volumes-demo"

services:
  dv-app1:
    image: dv-app:latest
    ports:
      - "5001:5000"
    volumes:
      - type: volume
        source: my-shared-volume
        target: /data
  dv-app2:
    image: dv-app2:latest
    ports:
      - "5002:5000"
    volumes:
      - type: volume
        source: my-shared-volume
        target: /data
        read_only: true

volumes:
  my-shared-volume:
```

The `volumes` top-level element creates the volume `my-shared-volume` for us if it does not exist already, so there's no need to run a separate docker CLI command to create the volume. Notice that we've specified two services: `dv-app1` and `dv-app2`, each will run their respective image and on their assigned ports, but mounted with the same volume. Also note that when specifying the volume mount for `dv-app2`, we've set an option named `read_only` to `true` to indicate that `dv-app2` container is not allowed to write data into the volume, but it can only read data from it. 

---

## Let's docker-compose!

We now have our main ingredients for shared-volume setup: two app images and `docker-compose.yml` file  that describes how to run the containers and mount a volume. Now we can run docker-compose simply by:

```
docker-compose up
```

You'll then get the following output indicating the order by which the components were created by docker-compose:

```
[+] Running 3/3
 ⠿ Network docker-volumes-demo_default      Created   0.0s
 ⠿ Container docker-volumes-demo-dv-app1-1  Created   0.1s
 ⠿ Container docker-volumes-demo-dv-app2-1  Created   0.1s
```

Below this message will be a standard Flask message telling you that `dv-app1` is running and listening for traffic on port 5001, and `dv-app2` is doing the same on port 5002.

You can now open up a browser window and visit `http://localhost:5001/upload`, which will take you to a basic HTML page containing an upload and a submit button.

![app1 upload endpoint]({{site.baseurl}}/assets/images/docker-compose-drawings/app1-upload-page.png){: width="400" loading="lazy" style="margin-bottom: 1em"}

I created a **`hello.txt`** file containing the following text and uploaded it to that form.

```
Hiii!!!
```

![app1 upload successful]({{site.baseurl}}/assets/images/docker-compose-drawings/app1-upload-success.png){: width="400" loading="lazy" style="margin-bottom: 1em"}

In a separate browser window, visit `http://localhost:5002/`, which will call the endpoint on `app2` that will display the data from the file that I just uploaded via `app1`.

![app2 root endpoint]({{site.baseurl}}/assets/images/docker-compose-drawings/app2-data-display.png){: width="340" loading="lazy" style="margin-bottom: 1em"}

`app2` was able to access the data that was uploaded through `app1` because they were mounted with the same volume. And, although we didn't write an endpoint in `app2` to write data into the volume, specifying the `readonly: true` option in the volume mount definition of this container restricts the container's permission on the volume to read-only.

---

<br />

In this article, we spun up two containerised apps and a docker volume, then mounted that volume onto the two containers' respective `/data` directory. The first app was configured to write data into the volume, while the second app read data from the volume. This demonstrates a foundational yet very powerful feature of dockerised applications in terms of data sharing, data integrity, and security. We also saw how docker-compose can step in and simplify the workflow of setting up multiple data-sharing containers, such that as your containerised architecture grows, maintaining and scaling your resources is still fairly easy to manage.
