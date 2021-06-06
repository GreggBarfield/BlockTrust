'use strict';

var express = require('express');
var bodyParser = require('body-parser');
var app = express();
const { connectGateway } = require('./fabricNetwork');
const { BlockDecoder } = require('fabric-common');

app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

const channelName = 'mychannel';
const chaincodeName = 'basic';

// create a record and save it into the blockchain
app.post('/api/add-record', async function (req, res) {
  try {

    if (!req.is('application/json')) {
      res.sendStatus(400)
    }

  let gateway = await connectGateway();
  // Build a network instance based on the channel where the smart contract is deployed
  let network = await gateway.getNetwork(channelName);
  let contract = network.getContract(chaincodeName);

    let tx = await contract.submitTransaction('CreateRecord', JSON.stringify(req.body.data));
    res.json({
      status: 'OK - Transaction has been submitted',
      record: JSON.parse(tx.toString())
    });
  await gateway.disconnect();
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
});

app.get('/api/get-record/:id', async function (req, res) {
  try {
    let gateway = await connectGateway();
    let network = await gateway.getNetwork(channelName);
    let contract = network.getContract(chaincodeName);
    
    const retVal = await contract.evaluateTransaction('ReadRecord', req.params.id.toString());
    let response = JSON.parse(retVal.toString());
    res.json({result:response});
    await gateway.disconnect();
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
})

app.get('/api/get-block/:txid', async function (req, res) {
  try {
    const gateway = await connectGateway();
    const network = await gateway.getNetwork(channelName);
    const contract = network.getContract('qscc');// Query System Chaincode
    const resultByte = await contract.evaluateTransaction(
      'GetBlockByTxID',
      channelName,
      req.params.txid.toString()
    );
    const resultJson = BlockDecoder.decode(resultByte);
    res.json(resultJson);
    await gateway.disconnect();
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
})

app.get('/api/get-transaction/:txid', async function (req, res) {
  try {
    const gateway = await connectGateway();
    const network = await gateway.getNetwork(channelName);
    const contract = network.getContract('qscc');
    const resultByte = await contract.evaluateTransaction(
      'GetTransactionByID',
      channelName,
      req.params.txid.toString()
  );
    const resultJson = BlockDecoder.decodeTransaction(resultByte);
    // to get the timestamp: resultJson.transactionEnvelope.payload.header.channel_header.timestamp
    res.json(resultJson);
    await gateway.disconnect();
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: errors
    });
  }
})


app.listen(3000, ()=>{
  console.log("*************************************************");
  console.log("Blockchain API server listening at localhost:3000");
  console.log("*************************************************");
});