#!/bin/bash
# This script is used to download the backup files to launch a network.

# tell the bash to exit when it receives signal SIGINT (when pressing Ctrl + C)
trap "exit" INT

# load helper functions for printing and help msg
. ../blockchain-network/scripts/utils.sh

infoln "********** Download Backup Files (blockchain credentials, log and other settings) **********"
infoln "You can press Ctrl+C to exit...\n"

infoln "Please provide the AWS configuration."
aws configure

infoln "Enter the source folder which contains the backup.zip in s3 bucket \"btnblockchainbackup\". (Don't include the slash after the directory name)"  
infoln "Sample input: 21-04-2021-01:05:25"
infoln "Enter the directory name in s3 here >>"
read s3_source  

mkdir -p ../backup

infoln "Download the files from s3://btnblockchainbackup/$s3_source/backup_$s3_source.zip."
aws s3 cp s3://btnblockchainbackup/$s3_source/backup_$s3_source.zip ../backup