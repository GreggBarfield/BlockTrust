//NOTE: Can't test the chaincode here as no transaction id is generated in testing when creating a record.

// 'use strict';
// const sinon = require('sinon');
// const chai = require('chai');
// const sinonChai = require('sinon-chai');
// const expect = chai.expect;

// const { Context } = require('fabric-contract-api');
// const { ChaincodeStub } = require('fabric-shim');

// const RecordManagementContract = require('../lib/recordManagementContract.js');

// let assert = sinon.assert;
// chai.use(sinonChai);

// describe('Record Management Basic Tests', () => {
//     let transactionContext, chaincodeStub, expected_record;
//     beforeEach(() => {
//         transactionContext = new Context();

//         chaincodeStub = sinon.createStubInstance(ChaincodeStub);
//         transactionContext.setChaincodeStub(chaincodeStub);

//         chaincodeStub.putState.callsFake((key, value) => {
//             if (!chaincodeStub.states) {
//                 chaincodeStub.states = {};
//             }
//             chaincodeStub.states[key] = value;
//         });

//         chaincodeStub.getState.callsFake(async (key) => {
//             let ret;
//             if (chaincodeStub.states) {
//                 ret = chaincodeStub.states[key];
//             }
//             return Promise.resolve(ret);
//         });

//         chaincodeStub.deleteState.callsFake(async (key) => {
//             if (chaincodeStub.states) {
//                 delete chaincodeStub.states[key];
//             }
//             return Promise.resolve(key);
//         });

//         chaincodeStub.getStateByRange.callsFake(async () => {
//             function* internalGetStateByRange() {
//                 if (chaincodeStub.states) {
//                     // Shallow copy
//                     const copied = Object.assign({}, chaincodeStub.states);

//                     for (let key in copied) {
//                         yield {value: copied[key]};
//                     }
//                 }
//             }

//             return Promise.resolve(internalGetStateByRange());
//         });

//         // we can't test txID here since we are not submitting a real transaction to the network
//         expected_record = {
//             data: 'initial data',
//             created: new Date(),
//         };

//     });

//     describe('Test CreateRecord', () => {
//         // NOTICE: this part doesn't throw the exception with the defined msg we specified
//         it('should return error on CreateRecord', async () => {
//             chaincodeStub.putState.rejects('failed inserting key');
//             let recordManagementContract = new RecordManagementContract();
//             try {
//                 await recordManagementContract.CreateRecord(transactionContext, expected_record.data);
//                 assert.fail('CreateRecord should have failed');
//             } catch(err) {
//                 expect(err.name).to.equal('failed inserting key');
//             }
//         });
//         it('should return success on CreateRecord', async () => {
//             let recordManagementContract = new RecordManagementContract();
//             let actual_record = await recordManagementContract.CreateRecord(transactionContext, expected_record.data);
//             const id = JSON.parse(actual_record.toString()).id;
//             let ret = JSON.parse((await chaincodeStub.getState(id)).toString());
//             // manually set the created time equal for testing
//             expected_record.created = ret.created;
//             expect(ret).to.eql(expected_record);
//         });
//     });

//     describe('Test ReadRecord', () => {
//         it('should return error on ReadRecord', async () => {
//             let recordManagementContract = new RecordManagementContract();
//             await recordManagementContract.CreateRecord(transactionContext, expected_record.data);

//             try {
//                 await recordManagementContract.ReadRecord(transactionContext, 'record2');
//                 assert.fail('ReadRecord should have failed');
//             } catch (err) {
//                 expect(err.message).to.equal('The record record2 does not exist');
//             }
//         });

//         it('should return success on ReadRecord', async () => {
//             let recordManagementContract = new RecordManagementContract();
//             let actual_record = await recordManagementContract.CreateRecord(transactionContext, expected_record.data);
//             const id = JSON.parse(actual_record.toString()).id;

//             let ret = JSON.parse(await chaincodeStub.getState(id));
//             // manually set the created time equal for testing
//             expected_record.created = ret.created;
//             expect(ret).to.eql(expected_record);
//         });
//     });

//     describe('Test DeleteRecord', () => {
//         it('should return error on DeleteRecord', async () => {
//             let recordManagementContract = new RecordManagementContract();

//             try {
//                 await recordManagementContract.DeleteRecord(transactionContext, 'record2');
//                 assert.fail('DeleteRecord should have failed');
//             } catch (err) {
//                 expect(err.message).to.equal('The record record2 does not exist');
//             }
//         });

//         it('should return success on DeleteRecord', async () => {
//             let recordManagementContract = new RecordManagementContract();
//             let actual_record = await recordManagementContract.CreateRecord(transactionContext, expected_record.data);
//             const id = JSON.parse(actual_record.toString()).id;

//             await recordManagementContract.DeleteRecord(transactionContext, id);
//             let ret = await chaincodeStub.getState(id);
//             expect(ret).to.equal(undefined);
//         });
//     });

//     describe('Test GetAllRecords', () => {
//         it('should return success on GetAllRecords', async () => {
//             let recordManagementContract = new RecordManagementContract();

//             let actual_record1 = await recordManagementContract.CreateRecord(transactionContext, 'data1');
//             let actual_record2 = await recordManagementContract.CreateRecord(transactionContext, 'data2');
//             let actual_record3 = await recordManagementContract.CreateRecord(transactionContext, 'data3');
//             let actual_record4 = await recordManagementContract.CreateRecord(transactionContext, 'data4');
//             let created1 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record1.toString()).id)).created;
//             let created2 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record2.toString()).id)).created;
//             let created3 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record3.toString()).id)).created;
//             let created4 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record4.toString()).id)).created;
//             let ret = await recordManagementContract.GetAllRecords(transactionContext);
//             console.log(actual_record1);
//             console.log(actual_record2);
//             console.log(actual_record3);
//             console.log(actual_record4);


//             ret = JSON.parse(ret);
//             // expect(ret.length).to.equal(4);

//             let expected = [
//                 {Record: { created: created1, data: 'data1'}},
//                 {Record: { created: created2, data: 'data2'}},
//                 {Record: { created: created3, data: 'data3'}},
//                 {Record: { created: created4, data: 'data4'}}
//             ];
//             console.log(expected);
//             expect(ret).to.eql(expected);
//         });

//         it('should return success on GetAllRecords for non JSON value', async () => {
//             let recordManagementContract = new RecordManagementContract();

//             chaincodeStub.putState.onFirstCall().callsFake((key, value) => {
//                 if (!chaincodeStub.states) {
//                     chaincodeStub.states = {};
//                 }
//                 chaincodeStub.states[key] = 'non-json-value';
//             });

//             await recordManagementContract.CreateRecord(transactionContext, 'data1');
//             let actual_record2 =await recordManagementContract.CreateRecord(transactionContext, 'data2');
//             let actual_record3 =await recordManagementContract.CreateRecord(transactionContext, 'data3');
//             let actual_record4 =await recordManagementContract.CreateRecord(transactionContext, 'data4');

//             let ret = await recordManagementContract.GetAllRecords(transactionContext);
//             ret = JSON.parse(ret);
//             expect(ret.length).to.equal(4);

//             let created2 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record2.toString()).id)).created;
//             let created3 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record3.toString()).id)).created;
//             let created4 = JSON.parse(await chaincodeStub.getState(JSON.parse(actual_record4.toString()).id)).created;

//             let expected = [
//                 {Record: 'non-json-value'},
//                 {Record: { created: created2, data: 'data2'}},
//                 {Record: { created: created3, data: 'data3'}},
//                 {Record: { created: created4, data: 'data4'}}
//             ];
//             expect(ret).to.eql(expected);
//         });
//     });
// });
