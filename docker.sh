#!/bin/sh
BASEDIR=`dirname $0`
cd $BASEDIR

docker build -t fdabrandao/pympl .
docker run -it -p 5555 fdabrandao/pympl
