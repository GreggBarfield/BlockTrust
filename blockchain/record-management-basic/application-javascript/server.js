'use strict';

var express = require('express');
var bodyParser = require('body-parser');
var app = express();
const fabricNetwork = require('./fabricNetwork')
const { BlockDecoder } = require('fabric-common');

app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));

const channelName = 'mychannel';
const chaincodeName = 'basic';


// create a record and save it into the blockchain
app.post('/api/addRecord', async function (req, res) {
  try {
    const network = await fabricNetwork.connectNetwork(channelName);
    const contract = network.getContract(chaincodeName);
    let tx = await contract.submitTransaction('CreateRecord', req.body.data);
    res.json({
      status: 'OK - Transaction has been submitted',
      record: JSON.parse(tx.toString())
    });
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }

});

app.get('/api/getRecord/:id', async function (req, res) {
  try {
    const network = await fabricNetwork.connectNetwork(channelName);
    const contract = network.getContract(chaincodeName);
    const result = await contract.evaluateTransaction('ReadRecord', req.params.id.toString());
    let response = JSON.parse(result.toString());
    res.json({result:response});
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
})

app.get('/api/getBlock/:txid', async function (req, res) {
  try {
    const network = await fabricNetwork.connectNetwork(channelName);
    const contract = network.getContract('qscc');// Query System Chaincode
    const resultByte = await contract.evaluateTransaction(
      'GetBlockByTxID',
      channelName,
      req.params.txid.toString()
    );
    const resultJson = BlockDecoder.decode(resultByte);
    res.json(resultJson);
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
})

app.get('/api/getTransaction/:txid', async function (req, res) {
  try {
    const network = await fabricNetwork.connectNetwork(channelName);
    const contract = network.getContract('qscc');
    const resultByte = await contract.evaluateTransaction(
      'GetTransactionByID',
      channelName,
      req.params.txid.toString()
  );
    const resultJson = BlockDecoder.decodeTransaction(resultByte);
    // to get the timestamp: resultJson.transactionEnvelope.payload.header.channel_header.timestamp
    res.json(resultJson);
  } catch (error) {
    console.error(`Failed to evaluate transaction: ${error}`);
    res.status(500).json({
      error: error
    });
  }
})



app.listen(3000, ()=>{
  console.log("*************************************************");
  console.log("Blockchain API server listening at localhost:3000");
  console.log("*************************************************");
});