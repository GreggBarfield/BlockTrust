import subprocess
import copy

"""
Have the environment configured ahead of time!
"""

setup = """
docker image build --tag api_deploy --file api/server/docker/dockerfile.aws ./
docker image save --output api/server/docker/api_deploy.image api_deploy
scp -i ~/Documents/LedgerSpace/keypairs/external-testing-key-pair.pem api/server/docker/api_deploy.image ubuntu@api.dev.blocktrustnetwork.com:~
rm api/server/docker/api_deploy.image
"""

ssh = ["ssh", "-i", "~/Documents/LedgerSpace/keypairs/external-testing-key-pair.pem", "ubuntu@api.dev.blocktrustnetwork.com"]

serverside = """
sudo docker image load -i api_deploy.image
sudo systemctl stop btn-api
sudo docker container rm api
sudo docker container create -p 127.0.0.1:5000:5000 --name api api_deploy
sudo systemctl start btn-api
sudo docker image prune -f
"""

commands = []


for line in setup.split("\n"):
    line = line.strip("\r ")

    if line != "":
        commands.append(line)

for line in serverside.split("\n"):
    line = line.strip("\r ")

    if line != "":
        sshc = copy.deepcopy(ssh)
        sshc += [line]
        commands.append(sshc)

for command in commands:
    print("Running", command)
    subprocess.run(command)
