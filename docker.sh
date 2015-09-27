#!/bin/sh
BASEDIR=`dirname $0`
cd $BASEDIR

docker build -t fdabrandao/pympl .
docker stop $(docker ps -a | grep fdabrandao/pympl | cut -d" " -f1)
docker rm $(docker ps -a | grep fdabrandao/pympl | cut -d" " -f1)
docker run -it -p 5555 fdabrandao/pympl
#docker run -it -p 5555 fdabrandao/pympl python -m pympl.webapp.app 5555 PASS
