Developing
==========

docker-compose -f core/docker/docker-compose.dev.yaml up --build --detach
docker-compose -f core/docker/docker-compose.dev.yaml stop
docker-compose -f core/docker/docker-compose.dev.yaml restart
docker-compose -f core/docker/docker-compose.dev.yaml stop && docker-compose -f core/docker/docker-compose.dev.yaml up --build --detach
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
