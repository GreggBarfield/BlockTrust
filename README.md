Developing
==========


Docker

Web development stack:
docker-compose -f core/docker/docker-compose.dev.yaml -p btn-core stop \
    && docker-compose -f core/docker/docker-compose.dev.yaml -p btn-core up --build --detach

Reports worker (requries web dev stack online):
docker-compose -f reports_worker/docker/docker-compose.dev.yaml -p btn-rw stop \
    && docker-compose -f reports_worker/docker/docker-compose.dev.yaml -p btn-rw up --build --detach

API:
    Translation worker:
        docker-compose -f api/translation_worker/docker/docker-compose.dev.yaml -p btn-api-tw stop \
            && docker-compose -f api/translation_worker/docker/docker-compose.dev.yaml -p btn-api-tw up --build --detach

        sudo docker container update --restart unless-stopped tw
        (When it runs into issues, it is exit-happy. Probably a good idea to auto restart it.)
    
    Server:
        docker-compose -f api/server/docker/docker-compose.dev.yaml -p btn-api-server stop \
            && docker-compose -f api/server/docker/docker-compose.dev.yaml -p btn-api-server up --build --detach


aing0Eitohy1yah3ang2Oapai6quu6Ge

'root'@'localhost' password: 09wg84j09843umgf0w934gj09w34g (dev computer)
'root'@'localhost' password: doojuiseeN6Quooph6yoosai6foh3fae (ledgerspacedev)

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


Testing
=========

pytest
pytest api/translation_worker


