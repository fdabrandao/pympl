#!/bin/sh

docker build -t fdabrandao/pympl .
docker run -it -p 5555 fdabrandao/pympl
