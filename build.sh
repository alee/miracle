#! /usr/bin/env bash

# uid=

# # Get file name and line number
# while test $# -gt 0
# do
# 	if [[ "$1" == "-uid" ]]; then
# 		shift
# 		uid="$1"
# 		shift
# 	fi
# done

# # Ensure that the line number is valid
# re='^[0-9]+$'
# if ! [[ $uid =~ $re ]]; then
#    echo "Error: invalid uid number" >&2; exit 1
# fi

# baseimages/min, base, r

#cd docker && docker build -t miracle/min --build-arg uid=$uid .

# generate custom dhparam.pem for logjam https://blog.cloudflare.com/logjam-the-latest-tls-vulnerability-explained/
openssl dhparam -out nginx/dhparam.pem 4096;
# make sure you copy server key and server crt to this directory
echo "Copy the SSL key and cert to nginx/ as server.crt and server.key before deployment (until we switch to lets encrypt)"
cd docker;
for dn in min base r;
do docker build -t miracle/$dn -f $dn.Dockerfile .;
done
cd ..;
docker-compose build
# in Dockerfile
# ARG uid
# adduser -u $uid

