/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Contract } = require('fabric-contract-api');

class RecordManagementContract extends Contract {

    async InitLedger(ctx) {
        const records = [
            {
                id: 'record1',
                created: new Date(),
                data: {name: 'abc', lat: 31.9686, lon: 99.9018}
            }
        ];

        for (const record of records) {
            record.docType = 'record';
            await ctx.stub.putState(record.id, Buffer.from(JSON.stringify(record)));
            console.info(`Record ${record.id} initialized`);
        }
    }

    // CreateRecord issues a new record to the world state with given details.
    async CreateRecord(ctx, id, docType, data) {
        const now = new Date();
        const record = {
            id: id,
            docType: docType,
            created: now,
            data: data
        };
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
        const now = new Date();
        // overwriting original record with new record
        const updatedRecord = {
            id: id,
            created: now,
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

    // // TransferRecord updates the owner field of record with given id in the world state.
    // async TransferRecord(ctx, id, newOwner) {
    //     const recordString = await this.ReadRecord(ctx, id);
    //     const record = JSON.parse(recordString);
    //     record.Owner = newOwner;
    //     return ctx.stub.putState(id, Buffer.from(JSON.stringify(record)));
    // }

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
