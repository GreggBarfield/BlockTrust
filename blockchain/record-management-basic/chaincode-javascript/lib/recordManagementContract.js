/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Contract } = require('fabric-contract-api');

class RecordManagementContract extends Contract {

    // CreateRecord issues a new record to the world state with given details.
    async CreateRecord(ctx, data) {

        const record = {
            data: JSON.parse(data),
            created: new Date(),
        };
        const txID = ctx.stub.getTxID();
        //The transaction ID uniquely identifies the transaction within the scope of the channel.
        ctx.stub.putState(txID, Buffer.from(JSON.stringify(record)));
        record.id = txID;
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

}

module.exports = RecordManagementContract;
