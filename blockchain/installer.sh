#!/bin/bash
# This script will install all required packages for running Hyperledger Fabric network and its client application using Node.js.

step=1

# load helper functions for printing and help msg
. blockchain-network/scripts/utils.sh || . utils.sh

infoln "$step. Updating packages on the system."
sudo yum -y update
successln "Updated packages on the system"
((step++))

infoln "$step. Installing curl."
sudo yum -y install curl
successln "Installed curl."
((step++))

infoln "$step. Installing Golang."
sudo yum -y install golang
successln "Installed Golang."
((step++))

infoln "$step. Setting Golang's environment variables."
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
successln "Golang's environment variables have been set."
((step++))

infoln "$step. Installing Docker"
sudo yum -y install docker
successln "Docker installed."
((step++))

infoln "$step. Starting the Docker daemon."
sudo systemctl start docker
successln "Docker daemon started."
((step++))

infoln "$step. Check whether Docker is running. You should see \"Active: active (running)\" from the output."
sudo service docker status
((step++))

infoln "$step. Starting Docker automatically at system boot."
sudo systemctl enable docker
successln "Started Docker automatically at system boot"
((step++))

infoln "$step. Adding user 'ec2-user' to group 'docker'."
sudo usermod -a -G docker ec2-user
successln "Added user 'ec2-user' to group 'docker'"
((step++))

infoln "$step. Installing docker-compose."
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
successln "Installed docker-compose."
((step++))

infoln "$step. Making docker-compose executable."
sudo chmod +x /usr/local/bin/docker-compose
successln "Made docker-compose executable."
((step++))

infoln "$step. Checking whether docker-compose is installed sucessfully."
docker-compose version
((step++))

infoln "$step. Installing node.js and check whether node is installed."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node
node -e "console.log('Running Node.js ' + process.version)"
successln "Installed node."
((step++))

infoln "$step. Switching node to version 14.13.1."
nvm install 14.13.1
successln "Switched node to 14.13.1"
((step++))

infoln "$step. Installing gcc. We need it to build node.js"
sudo yum -y install gcc-c++
successln "Installed gcc."
((step++))

infoln "$step. Installing jq."
sudo yum -y install jq
successln "Installed jq."
((step++))

warnln "In some cases, you may need to reboot your instance to provide permissions for the ec2-user to access the Docker daemon."

read -p "Type \"yes\" to reboot>> "

if [ "$REPLY" != "yes" ]; then
  exit
fi

sudo reboot