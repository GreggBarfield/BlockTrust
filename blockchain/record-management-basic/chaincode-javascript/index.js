/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

// const assetTransfer = require('./lib/assetTransfer');

// module.exports.AssetTransfer = assetTransfer;
// module.exports.contracts = [assetTransfer];


const RecordManagementContract = require('./lib/recordManagementContract');

module.exports.RecordManagementContract = RecordManagementContract;
module.exports.contracts = [RecordManagementContract];