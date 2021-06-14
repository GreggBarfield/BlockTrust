#!/bin/bash
# This script is used to upload important credentials to S3 bucket for backup purpose.
# These keys can be used to run the original built blockchain network.

# Reference: Batch upload files to the cloud
# https://aws.amazon.com/getting-started/hands-on/backup-to-s3-cli/

# tell the bash to exit when it receives signal SIGINT (when pressing Ctrl + C)
trap "exit" INT

# load helper functions for printing and help msg
. ../blockchain-network/scripts/utils.sh

infoln "********** Upload backup Files (blockchain credentials, log and other settings) **********"
infoln "You can press Ctrl+C to exit...\n"

infoln "Please provide the AWS configuration."
infoln "
# This will prompt you to enter AWS acces key and other settings.
# Sample output: 
# AWS Access Key ID [****************GBGK]: 
# AWS Secret Access Key [****************jOAS]: 
# Default region name [us-east-2]: 
# Default output format [json]:
" 
aws configure

# create a bucket btnblockchain
# aws s3 mb s3://btnblockchainbackup
destination=$(date +"%m-%d-%Y-%T")

echo "new dir $destination"

infoln "Zipping files or directories into backup.zip."
mkdir -p ../backup
sudo zip -r ../backup/backup_$destination.zip ../blockchain-network/basic.tar.gz ../blockchain-network/log.txt ../blockchain-network/organizations ../blockchain-network/system-genesis-block ../record-management-basic/application-javascript/wallet
infoln "Uploading backup_$destination.zip to s3 bucket: $destination"
aws s3 cp "../backup/backup_$destination.zip" s3://btnblockchainbackup/$destination/;

infoln "Make sure you can find the backup file in the s3 bucket."