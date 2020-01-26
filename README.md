# data-trial

**Please read this entire README before you begin**

Some proficiency with Git, Python, Django, and your terminal is assumed. No proficiency with Docker is assumed but it is suggested that you read [this](https://docs.docker.com/engine/docker-overview/) to get familiar with the vocabulary.

### Overview

This repository is an example of what a typical SportsHi application codebase might look like. It is organized around two containerization (Docker) environments: production and sandbox. Production represents the environment used when the application is deployed. Sandbox represents the environment used for development - typically done on your local machine. The notable items are...

- `sandbox`: Shell script that provides a number of useful commands for developing in the sandbox environment; in your terminal run `./sandbox` to see the full list of commands
- `production`: Shell script that provides a number of useful commands for running a production environment; you can safely ignore this file
- `docker/sandbox/`: Directory containing files used by Docker for the sandbox environment
- `docker/production/`: Directory containing files used by Docker for the production environment; you can safely ignore this directory
- `components/`: Directory containing any number of isolated source code directories, each of which represents a distinct container; in this example there is only one component, but multiple components are common for real world applications, such as a server and a reverse proxy
- `components/server/`: Directory containing the source code for a server, in this example a [Django](https://www.djangoproject.com/) server; **you should only need to edit the files in this folder**

### About the Django server

The Django server has been created for you in the `components/server/` directory. The Django project files are in `server/project/`. The server is already setup to connect with a PostgreSQL database that is automatically created for you in a separate container when you start the server using the command `./sandbox up`. You can kill the server using `./sandbox down`, which will also bring down the database and save its data. If you need to use the Django CLI, you can run commands using `./sandbox python manage.py ...`. For example, to update the database with your latest models you would run `./sandbox python manage.py migrate`. Note that these commands will be running **inside** a Docker container where the working directory is `server/`. To lint your Python code against the PEP 8 style guide run `./sandbox lint`. The contents of the database will persist across the container lifecycle, but if you ever want to start over you can reset it by running `./sandbox reset_database`. As a last resort you can nuke everything by running `./sandbox down ; docker system prune --all`

### Your task

Your task is to implement a simple REST API according to [this OAS3 API specification](https://app.swaggerhub.com/apis/sportshi-team/data-test/1.0.0#/). You should implement exactly to spec, nothing more nothing less. How you implement is entirely up to you; you can install any python modules you want (see the `requirements.txt` file), you can create any Django apps you want, etc. Writing tests is optional.

While developing you will want to interact with your API to test it. Run `./sandbox up` to automatically run any migrations and start the server - it will be available on `http://0.0.0.0:8000/`. How you make requests to your API is up to you, but some options are your terminal, web browser, or an API development tool like Postman.

Roughly, the steps you need to follow to complete this task are...

1. Clone this repository onto your machine
2. [Install Docker for your operating system](https://docs.docker.com/get-docker/) (if using Windows you may have an easier time running a Linux VM); note that you do not need to install Python, PostgreSQL, or any other software onto your machine
3. Start Docker
4. Open your terminal and cd into the repository
5. Run `./sandbox up` to start the database, run the default migrations, and start the server; the first time you run this will be slow as Docker will be starting from scratch
6. Visit `http://0.0.0.0:8000/` in your web browser to verify that the Django server is running
7. Edit the files in `components/server/...` to implement the API specification.

Additionally, your python code should conform to the PEP 8 style guide; you can see any mistakes by running `./sandbox lint`

If you think you need to edit any files outside of `components/server/...`, or if you feel the commands in the `sandbox` script are not enough, let a SportsHi engineer know and we may be able to help you.

### When you are done

 Once you have finished you need to make your repo available to a SportsHi engineer for review. You can push to your own GitHub account under public settings, or simply email a zip file. Whatever you do, let your SportsHi contact know how to access your repo. They will test your API to see if it implements the specification. The quality and organization of the code that you write will also be considered.
