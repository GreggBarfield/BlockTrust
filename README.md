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

