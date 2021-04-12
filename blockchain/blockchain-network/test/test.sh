#!/bin/bash
# in fabric-local/blockchain-network
# echo $PWD
export FABRIC_CFG_PATH=${PWD}/../../config/
# export CORE_PEER_MSPCONFIGPATH=${PWD}/../organizations/peerOrganizations/org1.blocktrustnetwork.com/
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER0_ORG1_CA
export CORE_PEER_MSPCONFIGPATH=${PWD}/../organizations/peerOrganizations/org1.blocktrustnetwork.com/users/Admin@org1.blocktrustnetwork.com/msp
export CORE_PEER_ADDRESS=localhost:7051
../../bin/peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.blocktrustnetwork.com --tls --cafile ${PWD}/../organizations/ordererOrganizations/blocktrustnetwork.com/orderers/orderer.blocktrustnetwork.com/msp/tlscacerts/tlsca.blocktrustnetwork.com-cert.pem -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/../organizations/peerOrganizations/org1.blocktrustnetwork.com/peers/peer0.org1.blocktrustnetwork.com/tls/ca.crt -c '{"function":"InitLedger","Args":[]}'

../../bin/peer chaincode query -C mychannel -n record -c '{"Args":["GetAllRecords"]}'
