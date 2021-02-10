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
    
    Server:
        docker-compose -f api/server/docker/docker-compose.dev.yaml -p btn-api-server stop \
            && docker-compose -f api/server/docker/docker-compose.dev.yaml -p btn-api-server up --build --detach


aing0Eitohy1yah3ang2Oapai6quu6Ge

ubuntu@ip-172-26-15-39:~$ sudo cat /etc/systemd/system/webhooks.service 
[Unit]
Description = Start webhooks uWSGI instance
After = network.target

[Service]
User = ubuntu
Group = www-data
WorkingDirectory = /home/ubuntu/current
ExecStart = /usr/local/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy = multi-user.target
ubuntu@ip-172-26-15-39:~$ 

>>> s3c = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4', region_name='us-east-2'))
>>> s3c.generate_presigned_url('get_object', Params={'Bucket': 'btndev', 'Key': 'tf'}, ExpiresIn=20)


'root'@'localhost' password: 09wg84j09843umgf0w934gj09w34g (dev computer)


'root'@'localhost' password: doojuiseeN6Quooph6yoosai6foh3fae (ledgerspacedev)

This file has been edited.
