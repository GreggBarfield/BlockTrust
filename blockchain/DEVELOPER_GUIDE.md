# ###################
# For PRODUCTION
# ###################

**Blockchain Network Structure**: one organization network setup with one peer, ordering service, and one certificate authority.

## Pre-requisites:

To better understand the workflow, it is recommended to read the relevant Hyperledger Fabric Tutorials:
Running Fabric Network: https://hyperledger-fabric.readthedocs.io/en/latest/test_network.html
Running Fabric Application: https://hyperledger-fabric.readthedocs.io/en/latest/write_first_app.html
You may also take a look at the ```PROJECT_FOLDER/blockchain/blockchain-network/network.sh```, a script to manage all the common workflows. You can run ```./network.sh -h``` to see the usage. 

The following are the steps required to bring up a blockchain network. Steps 1 - 3 are one-time setting.

1. Download docker images and binaries for Fabric v2.3.1 and Fabric CA v1.4.9. These version numbers have been set by default in the ```PROJECT_FOLDER/blockchain/blockchain-network/scripts/bootstrap.sh```. This command needs to be run ONLY ONCE because the files persist even after running ```./network.sh down```.
From directory ```PROJECT_FOLDER/blockchain/blockchain-network```, run the command:
```
./scripts/bootstrap.sh -s
```

2. Bring up the network. First, create the certificates and keys(if they don't exist in the destination folder) using Certificate Authorities. Then deploy Peer state database (CouchDB in this case).
From directory ```PROJECT_FOLDER/blockchain/blockchain-network/```, run the command:
```
./network.sh up createChannel -ca -s couchdb
```

3. Uses the chaincode lifecycle to package, install, query installed chaincode, approve chaincode for Org1,
and finally commit the chaincode. These are the actions to takes to deploy a chaincode to a channel. Use any of the record-management-basic chaincodes deployed on the channel "mychannel." with the chaincode name of "basic".
From directory ```PROJECT_FOLDER/blockchain/blockchain-network/```, run the command:
```
./network.sh deployCC -ccn basic -ccp ../record-management-basic/chaincode-javascript/ -ccl javascript
```

4. Make sure node.js is installed. 
```
node -v
```

5. Install code dependencies.
From directory ```PROJECT_FOLDER/blockchain/record-management-basic/application-javascript```, run the command:
```
npm install
```

6. Run the client application.
From directory ```PROJECT_FOLDER/blockchain/record-management-basic/application-javascript```, run the command:
```
node server.js
```
When the application is running for the first time. A new directory named "wallet" which contains the admin user and application user's credentials will be generated in the directory ```PROJECT_FOLDER/blockchain/record-management-basic/application-javascript/```

# ########################
# For Both PRODUCTION and DEVELOPMENT
# ########################

If you want to bring down the blockchain network, you can run the following command in ```PROJECT_FOLDER/blockchain/blockchain-network/```. WARNNING: You will be asked to type "yes" to confirm the action as this command will remove all the relevant containers about the blockchain network, unwanted images and generated credential materials. You can find the details in the function "networkDown" in ```PROJECT_FOLDER/blockchain/blockchain-network/network.sh```.
``` 
./network.sh down
```

# #######################
# For Local Testing
# #######################
Run the test application to see how sdk node.js works.
From directory ```PROJECT_FOLDER/blockchain/record-management-basic/application-javascript```, run the command:
```
node app.js
```

To see the sdk node.js code working, run the following command before running ```node app.js```:
```
export HFC_LOGGING='{"debug":"console"}'' 
```

# #######################
# IMPORTANT NOTES 
# #######################
1. **Wallet**
If you decide to start over by taking down the network and bringing it back up again, you will have to delete the wallet folder and its identities prior to re-running the javascript application or you will get an error. This happens because the Certificate Authority and its database are taken down when the blockchain network is taken down but the original wallet still remains in the application-javascript directory so it must be deleted. When you re-run the sample javascript application, a new wallet and credentials will be generated.

If you see  kind an error like these:
```
2020-08-07T20:23:17.590Z - error: [DiscoveryService]: send[mychannel] - Channel:mychannel received discovery error:access denied
******** FAILED to run the application: Error: DiscoveryService: mychannel error: access denied
```

   OR
```
Failed to register user : Error: fabric-ca request register failed with errors [[ { code: 20, message: 'Authentication failure' } ]]
******** FAILED to run the application: Error: Identity not found in wallet: appUser
```
Delete the ```PROJECT_FOLDER/blockchain/record-management-basic/application-javascript/wallet``` directory and retry this application. The certificate authority must have been restarted and the saved certificates for the admin and application user are not valid. Deleting the wallet store will force these to be reset with the new certificate authority.

2. **CouchDB**
In order to leverage the benefits of CouchDB, namely content-based JSON queries, your data must be modeled in JSON format. You must decide whether to use LevelDB or CouchDB before setting up your network. Switching a peer from using LevelDB to CouchDB is not supported due to data compatibility issues. All peers on the network must use the same database type. If you have a mix of JSON and binary data values, you can still use CouchDB, however the binary values can only be queried based on key, key range, and composite key queries.


# ##################
# Other Configuration 
# ##################

- **Set the Block size and Transaction** [link](https://stackoverflow.com/questions/52436847/block-size-and-transaction-per-block-in-hyperledger-fabric)\
In the Channel configuration file: 
```PROJECT_FOLDER/blockchain/blockchain-network/configtx/configtx.yaml```, you can modify the MaxMessageCount, AbsoluteMaxBytes and PreferredMaxBytes in the Orderer section.







