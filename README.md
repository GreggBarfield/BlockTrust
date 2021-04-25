# Resources

- BTN Developer Guide: https://docs.google.com/document/d/1rZRAPgqILzBfXDPBJQfGqnAsglGssID07MWHNJW1YS4/edit#

# Developing

## Web development stack

Starting the full local environment:

```bash
docker-compose -f core/docker/docker-compose.dev.yaml \
    -p btn-core stop \
&& docker-compose -f core/docker/docker-compose.dev.yaml \
    -p btn-core up --build --detach
```

## Reports worker
(connects to docker network btn-core_default)

```bash
docker-compose -f reports_worker/docker/docker-compose.dev.yaml \
    -p btn-rw stop \
&& docker-compose -f reports_worker/docker/docker-compose.dev.yaml \
    -p btn-rw up --build --detach
```

## API

### API Translation Worker

```bash
docker-compose -f api/translation_worker/docker/docker-compose.dev.yaml \
    -p btn-api-tw stop \
&& docker-compose -f api/translation_worker/docker/docker-compose.dev.yaml \
    -p btn-api-tw up --build --detach
```

### API Server
    
```bash
docker-compose -f api/server/docker/docker-compose.dev.yaml -p btn-api-server \
    stop \
&& docker-compose -f api/server/docker/docker-compose.dev.yaml \
    -p btn-api-server up --build --detach
```

# General Docker tips

## Building specific services

To build only specific services), add the service names after the docker-compose command but before the command options:

```bash
docker-compose -f core/docker/docker-compose.dev.yaml \
    -p btn-core stop webpack \
    && docker-compose -f core/docker/docker-compose.dev.yaml \
    -p btn-core up webpack --build --detach
```

## Persisting a container after restarts

```bash
docker container update --restart unless-stopped tw
```

# Internal Testing Deployments
Internal testing is made up of external-test-server-1 (lightsail), the external API server, and EC2 instance ledgerspacedev.com i-01390ee79c2452eb3, running most of the rest. There are also blockchain servers, but they don't need to be updated as frequently.

BTN developer guide has a bit of information on this.

### API Translation Worker
```bash
docker image build --tag tw --file api/translation_worker/docker/dockerfile.aws .
docker image save -o tw.image tw
scp -i ../aws/kp-ledgerspacedev.pem tw.image ubuntu@ledgerspacedev.com:~
rm tw.image
ssh -i ../aws/kp-ledgerspacedev.pem ubuntu@ledgerspacedev.com
sudo docker image load -i tw.image
rm tw.image
sudo docker container stop tw
sudo docker container rm tw
sudo docker container create --name tw --restart unless-stopped --env PYTHONUNBUFFERED=1 tw
sudo docker container start tw
sudo docker logs --tail 5 tw
exit
```


# Testing

```bash
pytest
pytest api/translation_worker
```

