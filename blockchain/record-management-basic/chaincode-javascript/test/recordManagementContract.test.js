'use strict';
const sinon = require('sinon');
const chai = require('chai');
const sinonChai = require('sinon-chai');
const expect = chai.expect;

const { Context } = require('fabric-contract-api');
const { ChaincodeStub } = require('fabric-shim');

const RecordManagementContract = require('../lib/recordManagementContract.js');

let assert = sinon.assert;
chai.use(sinonChai);

describe('Record Management Basic Tests', () => {
    let transactionContext, chaincodeStub, record;
    beforeEach(() => {
        transactionContext = new Context();

        chaincodeStub = sinon.createStubInstance(ChaincodeStub);
        transactionContext.setChaincodeStub(chaincodeStub);

        chaincodeStub.putState.callsFake((key, value) => {
            if (!chaincodeStub.states) {
                chaincodeStub.states = {};
            }
            chaincodeStub.states[key] = value;
        });

        chaincodeStub.getState.callsFake(async (key) => {
            let ret;
            if (chaincodeStub.states) {
                ret = chaincodeStub.states[key];
            }
            return Promise.resolve(ret);
        });

        chaincodeStub.deleteState.callsFake(async (key) => {
            if (chaincodeStub.states) {
                delete chaincodeStub.states[key];
            }
            return Promise.resolve(key);
        });

        chaincodeStub.getStateByRange.callsFake(async () => {
            function* internalGetStateByRange() {
                if (chaincodeStub.states) {
                    // Shallow copy
                    const copied = Object.assign({}, chaincodeStub.states);

                    for (let key in copied) {
                        yield {value: copied[key]};
                    }
                }
            }

            return Promise.resolve(internalGetStateByRange());
        });

        record = {
            id: 'record1',
            docType: 'record',
            created: new Date(),
            data: {name: 'abc', lat: 31.9686, lon: 99.9018}
        };
    });

    describe('Test InitLedger', () => {
        it('should return error on InitLedger', async () => {
            chaincodeStub.putState.rejects('failed inserting key');
            let recordManagementContract = new RecordManagementContract();
            try {
                await recordManagementContract.InitLedger(transactionContext);
                assert.fail('InitLedger should have failed');
            } catch (err) {
                expect(err.name).to.equal('failed inserting key');
            }
        });

        it('should return success on InitLedger', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.InitLedger(transactionContext);
            let ret = JSON.parse((await chaincodeStub.getState('record1')).toString());
            // manually set the created time equal for testing
            ret.created = record.created;
            expect(ret).to.eql(Object.assign({docType: 'record'}, record));
        });
    });

    describe('Test CreateRecord', () => {
        // NOTICE: this part doesn't throw the exception with the defined msg we specified
        it('should return error on CreateRecord', async () => {
            chaincodeStub.putState.rejects('failed inserting key');
            let recordManagementContract = new RecordManagementContract();
            try {
                await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);
                assert.fail('CreateRecord should have failed');
            } catch(err) {
                expect(err.name).to.equal('failed inserting key');
            }
        });

        it('should return success on CreateRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);
            let ret = JSON.parse((await chaincodeStub.getState(record.id)).toString());
            // manually set the created time equal for testing
            ret.created = record.created;
            expect(ret).to.eql(record);
        });
    });

    describe('Test ReadRecord', () => {
        it('should return error on ReadRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);

            try {
                await recordManagementContract.ReadRecord(transactionContext, 'record2');
                assert.fail('ReadRecord should have failed');
            } catch (err) {
                expect(err.message).to.equal('The record record2 does not exist');
            }
        });

        it('should return success on ReadRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);

            let ret = JSON.parse(await chaincodeStub.getState(record.id));
            // manually set the created time equal for testing
            ret.created = record.created;
            expect(ret).to.eql(record);
        });
    });

    describe('Test UpdateRecord', () => {
        it('should return error on UpdateRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);

            try {
                await recordManagementContract.UpdateRecord(transactionContext, 'record2', {name: 'def', lat: 28.9686, lon: 96.9018});
                assert.fail('UpdateRecord should have failed');
            } catch (err) {
                expect(err.message).to.equal('The record record2 does not exist');
            }
        });

        it('should return success on UpdateRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);

            await recordManagementContract.UpdateRecord(transactionContext, 'record1', {name: 'abc2', lat: 31.9686, lon: 99.9018});
            let ret = JSON.parse(await chaincodeStub.getState(record.id));
            let expected = {
                id: 'record1',
                data: {name: 'abc2', lat: 31.9686, lon: 99.9018},
                created: ret.created
            };
            expect(ret).to.eql(expected);
        });
    });

    describe('Test DeleteRecord', () => {
        it('should return error on DeleteRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);

            try {
                await recordManagementContract.DeleteRecord(transactionContext, 'record2');
                assert.fail('DeleteRecord should have failed');
            } catch (err) {
                expect(err.message).to.equal('The record record2 does not exist');
            }
        });

        it('should return success on DeleteRecord', async () => {
            let recordManagementContract = new RecordManagementContract();
            await recordManagementContract.CreateRecord(transactionContext, record.id, record.docType, record.data);

            await recordManagementContract.DeleteRecord(transactionContext, record.id);
            let ret = await chaincodeStub.getState(record.id);
            expect(ret).to.equal(undefined);
        });
    });

    describe('Test GetAllRecords', () => {
        it('should return success on GetAllRecords', async () => {
            let recordManagementContract = new RecordManagementContract();

            await recordManagementContract.CreateRecord(transactionContext, 'record1', 'record', {name: 'abc', lat: 31.9686, lon: 99.9018});
            await recordManagementContract.CreateRecord(transactionContext, 'record2', 'record', {name: 'def', lat: 32.9686, lon: 100.9018});
            await recordManagementContract.CreateRecord(transactionContext, 'record3', 'record', {name: 'ghi', lat: 33.9686, lon: 101.9018});
            await recordManagementContract.CreateRecord(transactionContext, 'record4', 'record', {name: 'jkl', lat: 34.9686, lon: 102.9018});
            let created1 = JSON.parse(await chaincodeStub.getState('record1')).created;
            let created2 = JSON.parse(await chaincodeStub.getState('record2')).created;
            let created3 = JSON.parse(await chaincodeStub.getState('record3')).created;
            let created4 = JSON.parse(await chaincodeStub.getState('record4')).created;
            let ret = await recordManagementContract.GetAllRecords(transactionContext);
            ret = JSON.parse(ret);
            expect(ret.length).to.equal(4);

            let expected = [
                {Record: {id: 'record1', docType: 'record', created: created1, data: {name: 'abc', lat: 31.9686, lon: 99.9018}}},
                {Record: {id: 'record2', docType: 'record', created: created2, data: {name: 'def', lat: 32.9686, lon: 100.9018}}},
                {Record: {id: 'record3', docType: 'record', created: created3, data: {name: 'ghi', lat: 33.9686, lon: 101.9018}}},
                {Record: {id: 'record4', docType: 'record', created: created4, data: {name: 'jkl', lat: 34.9686, lon: 102.9018}}}
            ];
            expect(ret).to.eql(expected);
        });

        it('should return success on GetAllRecords for non JSON value', async () => {
            let recordManagementContract = new RecordManagementContract();

            chaincodeStub.putState.onFirstCall().callsFake((key, value) => {
                if (!chaincodeStub.states) {
                    chaincodeStub.states = {};
                }
                chaincodeStub.states[key] = 'non-json-value';
            });

            await recordManagementContract.CreateRecord(transactionContext, 'record1', 'record', {name: 'abc', lat: 31.9686, lon: 99.9018});
            await recordManagementContract.CreateRecord(transactionContext, 'record2', 'record', {name: 'def', lat: 32.9686, lon: 100.9018});
            await recordManagementContract.CreateRecord(transactionContext, 'record3', 'record', {name: 'ghi', lat: 33.9686, lon: 101.9018});
            await recordManagementContract.CreateRecord(transactionContext, 'record4', 'record', {name: 'jkl', lat: 34.9686, lon: 102.9018});

            let ret = await recordManagementContract.GetAllRecords(transactionContext);
            ret = JSON.parse(ret);
            expect(ret.length).to.equal(4);

            let created2 = JSON.parse(await chaincodeStub.getState('record2')).created;
            let created3 = JSON.parse(await chaincodeStub.getState('record3')).created;
            let created4 = JSON.parse(await chaincodeStub.getState('record4')).created;

            let expected = [
                {Record: 'non-json-value'},
                {Record: {id: 'record2', docType: 'record', created: created2, data: {name: 'def', lat: 32.9686, lon: 100.9018}}},
                {Record: {id: 'record3', docType: 'record', created: created3, data: {name: 'ghi', lat: 33.9686, lon: 101.9018}}},
                {Record: {id: 'record4', docType: 'record', created: created4, data: {name: 'jkl', lat: 34.9686, lon: 102.9018}}}
            ];
            expect(ret).to.eql(expected);
        });
    });
});
