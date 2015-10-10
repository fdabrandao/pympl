#!/bin/sh
BASEDIR=`dirname $0`
cd $BASEDIR

docker build -t fdabrandao/pympl . || exit 1
docker stop $(docker ps -a | grep fdabrandao/pympl | cut -d" " -f1) 2>/dev/null
docker rm $(docker ps -a | grep fdabrandao/pympl | cut -d" " -f1) 2>/dev/null
docker run -it --rm -p 5555 fdabrandao/pympl || exit 1
#docker run -it --rm -p 5555 fdabrandao/pympl python -m pympl.webapp.app 5555 PASS
