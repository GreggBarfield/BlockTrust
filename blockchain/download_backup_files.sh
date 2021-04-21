#!/bin/bash
# This script is used to download the backup files to launch a network.

# load helper functions for printing and help msg
. blockchain-network/scripts/utils.sh || . utils.sh

aws configure

infoln "Enter the source folder which contains the backup.zip in s3 bucket \"btnblockchainbackup\". (Don't include the slash after the directory name)"  
infoln "Sample input: 21-04-2021-01:05:25"
read s3_source  

mkdir -p backup

infoln "Download the files from s3://btnblockchainbackup/$s3_source/backup.zip."
aws s3 cp s3://btnblockchainbackup/$s3_source/backup.zip ./backup