# nynorsk-rimordbok

Nynorsk rimordbok på nett

[![Build status](https://img.shields.io/circleci/project/github/iver56/nynorsk-rimordbok/master.svg)](https://circleci.com/gh/iver56/nynorsk-rimordbok) [![Code coverage](https://img.shields.io/codecov/c/github/iver56/nynorsk-rimordbok/master.svg)](https://codecov.io/gh/iver56/nynorsk-rimordbok)

# Setup

Install python 3.6

Install requirements: `pip install -r requirements.txt`

# Development

Run server: `python web_app.py`

## Code style

Format your python code with `black`. Set up your IDE to obey `.editorconfig`.

## Docker

Build docker image: `docker build -t nynorsk-rimordbok .`

Run docker image: `docker run --rm -it -p 80:80 nynorsk-rimordbok`

Now go to http://localhost to see if it works

## Testing

Run tests: `pytest`

# Deployment

First, check that the latest commit is green (i.e. the tests are OK). CircleCI is in charge of running the tests.

Docker images get built automatically by Docker Hub after commits are pushed to master. Check that the latest build succeeded.

If you are setting up the server for the first time, run the following commands (after replacing
email@example.org with your actual email address):

```
docker run --detach \
    --name nginx-proxy \
    --publish 80:80 \
    --publish 443:443 \
    --volume /etc/nginx/certs \
    --volume /etc/nginx/vhost.d \
    --volume /usr/share/nginx/html \
    --volume /var/run/docker.sock:/tmp/docker.sock:ro \
    --restart always \
    jwilder/nginx-proxy

docker run --detach \
    --name nginx-proxy-letsencrypt \
    --volumes-from nginx-proxy \
    --volume /var/run/docker.sock:/var/run/docker.sock:ro \
    --env "DEFAULT_EMAIL=email@example.org" \
    --restart always \
    jrcs/letsencrypt-nginx-proxy-companion

docker run --detach \
    --name nynorsk-rimordbok \
    --env "VIRTUAL_HOST=nynorskrimordbok.no" \
    --env "LETSENCRYPT_HOST=nynorskrimordbok.no" \
    --restart always \
    iverjo/nynorsk-rimordbok
```

If these containers are already running on the server, and you want to deploy the latest version
of the `iverjo/nynorsk-rimordbok` image, run this command instead:

```
docker pull iverjo/nynorsk-rimordbok && docker stop nynorsk-rimordbok && docker rm nynorsk-rimordbok && docker run --detach --name nynorsk-rimordbok --env "VIRTUAL_HOST=nynorskrimordbok.no" --env "LETSENCRYPT_HOST=nynorskrimordbok.no" iverjo/nynorsk-rimordbok
```
