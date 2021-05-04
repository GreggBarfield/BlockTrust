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

## New Deployments

### Updating Deployment

Update current branch:
```bash
ssh -i ../secrets/kp-ledgerspacedev.pem ubuntu@ledgerspacedev.com "cd LedgerSpace/blocktrust && git pull"
```

Switch branches:
```bash
ssh -i ../secrets/kp-ledgerspacedev.pem ubuntu@ledgerspacedev.com "cd LedgerSpace/blocktrust && git fetch && git checkout <branch>"
```

Rebuild containers:

Note: this does the production-style deployment, so 

```bash
ssh -i ../secrets/kp-ledgerspacedev.pem ubuntu@ledgerspacedev.com "cd LedgerSpace/blocktrust && docker-compose -f core/docker/docker-compose.aws.yaml -p btn-core build --no-cache && docker-compose -f core/docker/docker-compose.aws.yaml -p btn-core up --detach"
```


### Background

Created a new keypair:
`ssh-keygen`

Then copied it to the server:
`scp ../secrets/internal_deployments_bitbucket_ak* "ubuntu@ledgerspacedev.com:~/LedgerSpace/secrets"`

Fixed permissions:
`chmod 600 secrets/int*`

Added keypair to bitbucket access keys.

Set identity:
`nano ~/.ssh/config`

```
Host bitbucket.org
    IdentityFile ~/LedgerSpace/secrets/internal_deployments_bitbucket_ak
```

Clone:
`git clone git@bitbucket.org:blocktrust/blocktrust.git`

## Docker Contexts

Some remote operations can be done through docker contexts.

### Configuring keypairs

```bash
eval `ssh-agent -s`
ssh-add ../secrets/kp-ledgerspacedev.pem
```

On the remote server, sign in and run:
```bash
sudo usermod -aG docker $USER
```

Now you should be able to run locally:
```bash
docker --host "ssh://ubuntu@ledgerspacedev.com" ps
```

### Deploying core

Note: your docker for windows must be running locally


# Testing

```bash
pytest
pytest api/translation_worker
```

