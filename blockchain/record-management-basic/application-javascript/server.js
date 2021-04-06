var express = require('express');
var bodyParser = require('body-parser');
var app = express();
const fabricNetwork = require('./fabricNetwork')
app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));


app.post('/api/addRecord', async function (req, res) {

  try {
    const contract = await fabricNetwork.connectNetwork();
    // let record = {
    //   id: req.body.id,
    //   docType: req.body.docType,
    //   data: req.body.data
    // }
    let tx = await contract.submitTransaction('CreateRecord', req.body.id, req.body.docType, JSON.stringify(req.body.data));
    res.json({
      status: 'OK - Transaction has been submitted',
      txid: tx.toString()
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
    const contract = await fabricNetwork.connectNetwork();
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



app.listen(3000, ()=>{
  console.log("***********************************");
  console.log("API server listening at localhost:3000");
  console.log("***********************************");
});