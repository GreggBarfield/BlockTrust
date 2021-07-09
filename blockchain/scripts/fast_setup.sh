#!/bin/bash
# A menu driven shell script to execute commands.

## ----------------------------------
# Step #1: Define variables
# ----------------------------------
RED='\033[0;41;30m'
STD='\033[0;0;39m'

. ../blockchain-network/scripts/utils.sh

echo "current working directory: ${PWD}"
BLOCKCHAIN_ROOT="${PWD}/.."
echo "blockchain path: ${BLOCKCHAIN_ROOT}"
 
# ----------------------------------
# Step #2: User defined function
# ----------------------------------
pause(){
  read -p "Press [Enter] key to continue..." fackEnterKey
}

RedeployChaincode(){
	echo "RedeployChaincode() called"
        pause
      
	cd ${BLOCKCHAIN_ROOT}/blockchain-network

	infoln "Bringing up the blockchain network..."
	
	infoln "Creating peer node and channel..."
  ./network.sh up createChannel -ca -s couchdb

	infoln "Inspecting the external volumes..."
  docker volume inspect peer0.org1.blocktrustnetwork.com
  docker volume inspect orderer.blocktrustnetwork.com

	infoln "Deploying chaincode..."
  ./network.sh deployCC -ccn basic -ccp ../record-management-basic/chaincode-javascript/ -ccl javascript

  cd  ${BLOCKCHAIN_ROOT}/record-management-basic/application-javascript/

	infoln "Deleting old credentails in wallet..."
  rm -rf wallet/

	infoln "Enrolling admin and user..."
  node adminUserSetup.js

	infoln "Deleting old server and starting new server..."
  pm2 delete server
  pm2 start server.js
}
 
BingDownBlockchainNetwork(){
	echo "BingDownBlockchainNetwork() called"
        pause
	if [ -f /sys/hypervisor/uuid ] && [ `head -c 3 /sys/hypervisor/uuid` == ec2 ]; then
    warnln "This is running in ec2 instance. To protect the blockchain data, you can only run these commands manually."
		return
	fi

	cd ${BLOCKCHAIN_ROOT}/blockchain-network

	infoln "Bringing down the blockchain network..."
	./network.sh down
	infoln "Removing the external containers: peer0.org1.blocktrustnetwork.com, orderer.blocktrustnetwork.comorderer.blocktrustnetwork.com..."
	pause
	docker volume rm orderer.blocktrustnetwork.com
	docker volume rm peer0.org1.blocktrustnetwork.com
}

TestChaincode(){
	echo "TestChaincode() called"
        pause
	cd ${BLOCKCHAIN_ROOT}/record-management-basic/chaincode-javascript

	infoln "Testing chaincode..."
	npm test
}
 
# function to display menus
show_menus() {
	# clear
	echo "~~~~~~~~~~~~~~~~~~~~~"	
	echo " M A I N - M E N U"
	echo "~~~~~~~~~~~~~~~~~~~~~"
	echo "1. Redeploy chaincode (DEV and PROD. Do this if all the required packages are installed and the blockchain network was run successfully once.)"
	echo "2. Bring down blockchain network (DEV)"
	echo "3. Test chaincode (DEV)"
	echo "4. Exit"
	echo "~~~~~~~~~~~~~~~~~~~~~"
}

read_options(){
	local choice
	read -p "Enter choice [ 1 - 4] " choice
	case $choice in
		1) RedeployChaincode ;;
		2) BingDownBlockchainNetwork ;;
		3) TestChaincode ;;
		4) exit 0;;
		*) echo -e "${RED}Error...${STD}" && sleep 2
	esac
}
 
# ----------------------------------------------
# Step #3: Trap CTRL+C, CTRL+Z and quit singles
# ----------------------------------------------
trap '' SIGINT SIGQUIT SIGTSTP
 
# -----------------------------------
# Step #4: Main logic - infinite loop
# ------------------------------------
while true
do
 
	show_menus
	read_options
done