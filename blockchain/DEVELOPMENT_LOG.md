1. Storage considerations (https://hyperledger-fabric.readthedocs.io/en/release-2.2/deploypeer/peerplan.html)
Chaincodes and the ledger (one for each channel) are physically stored on a peer according to the peer.fileSystemPath parameter, while identities and MSP are stored according to the peer.mspConfigPath parameter (by default, both locations are at /var/hyperledger/production). This file system needs to be protected, secured, and writable by authorized users only and should also be regularly backed up. Note that the best practice is to use externally mounted volumes for both of these parameters, as they will therefore be easy to reference when restarting or upgrading the peer.

1.1 https://chat.hyperledger.org/home
You must provision persistent storage for your ledger files. The following properties in core.yaml dictates where ledger files and snapshots are written:

peer.fileSystemPath - defaults to /var/hyperledger/production
ledger.snapshots.rootDir - defaults to /var/hyperledger/production/snapshots

2. Change peer's state database password in docker-compose-couch.yaml

3. Change CA passwords in the following files
blockchain/application-utils/javascript/CAUtil.js
blockchain/blockchain-network/docker/docker-compose-ca.yaml
blockchain/blockchain-network/organizations/fabric-ca/registerEnroll.sh
blockchain/blockchain-network/organizations/fabric-ca/ordererOrg/fabric-ca-server-config.yaml
blockchain/blockchain-network/organizations/fabric-ca/org1/fabric-ca-server-config.yaml

4. Change identities' passwords in blockchain/blockchain-network/organizations/fabric-ca/registerEnroll.sh


4. Change localMspId from SampleOrg to Org1MSP in core.yaml


5. Ordering node for production
	- Set TLS to true
	- General.LocalMSPDir -> The best practice is to store this data in persistent storage.
	- Set LocalMSPID to OrdererMSP
	- Set FileLedger.Location -> The best practice is to store this data in persistent storage. This prevents the ledger from being lost if your orderer containers are destroyed for some reason.
	- set Admin.TLS.Enabled to true

- How to Deploy a Node.js Application On AWS EC2 Server
https://ourcodeworld.com/articles/read/977/how-to-deploy-a-node-js-application-on-aws-ec2-server



- Good practices for db queries
https://hyperledger-fabric.readthedocs.io/en/latest/couchdb_as_state_database.html#good-practices-for-queries