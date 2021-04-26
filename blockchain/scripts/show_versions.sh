#!/bin/bash
# This script prints installed packages'versions. 

. blockchain-network/scripts/utils.sh

infoln "curl version:"
curl --version
infoln ""

infoln "Golang version:"
go version
infoln ""

infoln "Python version:"
python -V
infoln ""

infoln "Node version:"
node -v
infoln ""

infoln "npm version:"
npm -version
infoln ""

infoln "Docker version:"
docker --version
infoln ""

infoln "Docker-compose version:"
docker-compose --version
infoln ""

###############
# Sample Output
###############

infoln "The sample output is for your reference."
infoln "Make sure you have the correct version for Node.js."
infoln ""
infoln "#################################"
infoln "######### Sample Output #########"
infoln "#################################"

infoln "
./version_check.sh: line 4: blockchain-network/scripts/utils.sh: No such file or directory
curl version:
curl 7.61.1 (x86_64-koji-linux-gnu) libcurl/7.61.1 OpenSSL/1.0.2k zlib/1.2.7 libidn2/2.3.0 libssh2/1.4.3 nghttp2/1.41.0
Release-Date: 2018-09-05
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp scp sftp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IDN IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz HTTP2 UnixSockets HTTPS-proxy Metalink 

Golang version:
go version go1.15.8 linux/amd64

Python version:
Python 2.7.18

Node version:
v14.13.1

npm version:
7.7.6

Docker version:
Docker version 19.03.13-ce, build 4484c46

Docker-compose version:
docker-compose version 1.29.1, build c34c88b2
"

infoln "########################################"
infoln "######### End of Sample Output #########"
infoln "########################################"

