/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 * 
 * Modified to return gateway.
 */

'use strict';

const { Gateway, Wallets } = require('fabric-network');
const FabricCAServices = require('fabric-ca-client');
const path = require('path');
const { buildCAClient, registerAndEnrollUser, enrollAdmin } = require('../../application-utils/javascript/CAUtil.js');
const { buildCCPOrg1, buildWallet } = require('../../application-utils/javascript/AppUtil.js');

const channelName = 'mychannel';
// const chaincodeName = 'basic';
const mspOrg1 = 'Org1MSP';
const org1UserId = 'appUser';
const walletPath = path.join(__dirname, 'wallet');

function prettyJSONString(inputString) {
	return JSON.stringify(JSON.parse(inputString), null, 2);
}

exports.enrollMyAdmin = async () => {

  // build an in memory object with the network configuration (also known as a connection profile)
  const ccp = buildCCPOrg1();

  // build an instance of the fabric ca services client based on
  // the information in the network configuration
  const caClient = buildCAClient(FabricCAServices, ccp, 'ca.org1.blocktrustnetwork.com');

  // setup the wallet to hold the credentials of the application user
  const wallet = await buildWallet(Wallets, walletPath);

  // in a real application this would be done on an administrative flow, and only once
  await enrollAdmin(caClient, wallet, mspOrg1);

}

exports.enrollUser = async(org1UserId) => {
    // build an in memory object with the network configuration (also known as a connection profile)
    const ccp = buildCCPOrg1();

    // build an instance of the fabric ca services client based on
    // the information in the network configuration
    const caClient = buildCAClient(FabricCAServices, ccp, 'ca.org1.blocktrustnetwork.com');
  
    // setup the wallet to hold the credentials of the application user
    const wallet = await buildWallet(Wallets, walletPath);
  
    // in a real application this would be done only when a new user was required to be added
    // and would be part of an administrative flow
    await registerAndEnrollUser(caClient, wallet, mspOrg1, org1UserId, 'org1.department1');
}

exports.connectGateway = async() => {

		// build an in memory object with the network configuration (also known as a connection profile)
		const ccp = buildCCPOrg1();

		// setup the wallet to hold the credentials of the application user
		const wallet = await buildWallet(Wallets, walletPath);

		// Create a new gateway instance for interacting with the fabric network.
		// In a real application this would be done as the backend server session is setup for
		// a user that has been verified.
		const gateway = new Gateway();

		
    // setup the gateway instance
    // The user will now be able to create connections to the fabric network and be able to
    // submit transactions and query. All transactions submitted by this gateway will be
    // signed by this user using the credentials stored in the wallet.
    await gateway.connect(ccp, {
      wallet,
      identity: org1UserId,
      discovery: { enabled: true, asLocalhost: true } // using asLocalhost as this gateway is using a fabric network deployed locally
    });

    return gateway;

}
