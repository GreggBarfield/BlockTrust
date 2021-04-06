#!/bin/bash
# in fabric-local/blockchain-network
../bin/peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.blocktrustnetwork.com --tls --cafile ${PWD}/organizations/ordererOrganizations/blocktrustnetwork.com/orderers/orderer.blocktrustnetwork.com/msp/tlscacerts/tlsca.blocktrustnetwork.com-cert.pem -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.blocktrustnetwork.com/peers/peer0.org1.blocktrustnetwork.com/tls/ca.crt -c '{"function":"InitLedger","Args":[]}'

../bin/peer chaincode query -C mychannel -n record -c '{"Args":["GetAllRecords"]}'
