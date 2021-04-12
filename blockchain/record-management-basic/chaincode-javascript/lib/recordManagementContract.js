/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Contract } = require('fabric-contract-api');

class RecordManagementContract extends Contract {

    // CreateRecord issues a new record to the world state with given details.
    async CreateRecord(ctx, id, data) {

        const record = {
            txID: ctx.stub.getTxID(),
            data: data,
            created: new Date(),
        };
        //The transaction ID uniquely identifies the transaction within the scope of the channel.
        ctx.stub.putState(id, Buffer.from(JSON.stringify(record)));
        return JSON.stringify(record);
    }

    // ReadRecord returns the record stored in the world state with given id.
    async ReadRecord(ctx, id) {
        const recordJSON = await ctx.stub.getState(id); // get the record from chaincode state

        if (!recordJSON || recordJSON.length === 0) {
            throw new Error(`The record ${id} does not exist`);
        }
        return recordJSON.toString();
    }

    // UpdateRecord updates an existing record in the world state with provided parameters.
    async UpdateRecord(ctx, id, data) {
        const exists = await this.RecordExists(ctx, id);
        if (!exists) {
            throw new Error(`The record ${id} does not exist`);
        }
        // overwriting original record with new record
        const updatedRecord = {
            txID: ctx.stub.getTxID(),
            created: new Date(),
            data: data
        };
        return ctx.stub.putState(id, Buffer.from(JSON.stringify(updatedRecord)));
    }

    // DeleteRecord deletes an given record from the world state.
    async DeleteRecord(ctx, id) {
        const exists = await this.RecordExists(ctx, id);
        if (!exists) {
            throw new Error(`The record ${id} does not exist`);
        }
        return ctx.stub.deleteState(id);
    }

    // RecordExists returns true when record with given id exists in world state.
    async RecordExists(ctx, id) {
        const recordJSON = await ctx.stub.getState(id);
        return recordJSON && recordJSON.length > 0;
    }

    // GetAllRecords returns all records found in the world state.
    async GetAllRecords(ctx) {
        const allResults = [];
        // range query with empty string for startKey and endKey does an open-ended query of all records in the chaincode namespace.
        const iterator = await ctx.stub.getStateByRange('', '');
        let result = await iterator.next();
        while (!result.done) {
            const strValue = Buffer.from(result.value.value.toString()).toString('utf8');
            let record;
            try {
                record = JSON.parse(strValue);
            } catch (err) {
                console.log(err);
                record = strValue;
            }
            allResults.push({ Key: result.value.key, Record: record });
            result = await iterator.next();
        }
        return JSON.stringify(allResults);
    }

    async GetBlock(ctx, txID) {
        const block = await queryBlockByTxID(txID);
        return block;
    }


}

module.exports = RecordManagementContract;
