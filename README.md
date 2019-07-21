# nynorsk-rimordbok

Nynorsk rimordbok på nett

[![Build status](https://img.shields.io/circleci/project/github/iver56/nynorsk-rimordbok/master.svg)](https://circleci.com/gh/iver56/nynorsk-rimordbok) [![Code coverage](https://img.shields.io/codecov/c/github/iver56/nynorsk-rimordbok/master.svg)](https://codecov.io/gh/iver56/nynorsk-rimordbok)

# Setup

Install python 3.6

Install requirements: `pip install -r requirements.txt`

# Usage

Run server: `python web_app.py`

# Development

## Code style

Format your python code with `black`. Set up your IDE to obey `.editorconfig`.

## Docker

Build docker image: `docker build -t nynorsk-rimordbok .`

Run docker image: `docker run -d -p 80:80 --name="nynorsk-rimordbok" nynorsk-rimordbok`

Now go to http://localhost to see if it works

## Testing

Run tests: `pytest`

# Deployment

First, check that the latest commit is green (i.e. the tests are OK). CircleCI is in charge of running the tests.

Docker images get built automatically by Docker Hub after commits are pushed to master. Check that the latest build succeeded.

To deploy the latest docker image, run `docker pull iverjo/nynorsk-rimordbok && docker stop nynorsk-rimordbok && docker rm nynorsk-rimordbok && docker run -d -p 80:80 --name="nynorsk-rimordbok" iverjo/nynorsk-rimordbok` on the production VM.
