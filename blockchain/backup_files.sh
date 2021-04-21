#!/bin/bash
# This script is used to upload important credentials to S3 bucket for backup purpose.
# These keys can be used to run the original built blockchain network.

# Reference: Batch upload files to the cloud
# https://aws.amazon.com/getting-started/hands-on/backup-to-s3-cli/

# load helper functions for printing and help msg
. blockchain-network/scripts/utils.sh || . utils.sh

aws configure

# create a bucket btnblockchain
# aws s3 mb s3://btnblockchainbackup
destination=$(date +"%d-%m-%Y-%T")

echo "new dir $destination"

infoln "Zipping files or directories into backup.zip."
sudo zip -r backup.zip blockchain-network/basic.tar.gz blockchain-network/log.txt blockchain-network/organizations blockchain-network/system-genesis-block

infoln "Uploading backup.zip to s3 bucket. $destination"
aws s3 cp "./backup.zip" s3://btnblockchainbackup/$destination/;