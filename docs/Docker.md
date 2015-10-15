## Docker

Docker is an open platform for building, shipping and running applications. Docker allows [PyMPL](https://github.com/fdabrandao/pympl) to run on a large variety of platforms with very little effort.

### Docker Setup
Install Docker [[Docker installation instructions](https://docs.docker.com/installation/)].

Option 1: simply `pull` PyMPL from Docker repository (without building):

```bash
user@locahost ~$ docker pull fdabrandao/pympl
```

Option 2: `clone` PyMPL and `build` locally:

```bash 
user@locahost ~$ git clone git@github.com:fdabrandao/pympl.git pympl
user@locahost ~$ docker build -t fdabrandao/pympl pympl
```

### Usage
Directly using the command line interface:

```bash
user@locahost ~$ docker run --rm -it fdabrandao/pympl bash
root@55d14f6b6f32:~# source venv2.7/bin/activate # load a virtualenv
(venv2.7)root@55d14f6b6f32:~# python examples/equivknapsack01.py
...
```

or through the PyMPL Web App (example URL: `http://172.17.0.60:5555/`):

```bash
user@locahost ~$ docker run --rm -it -p 5555 fdabrandao/pympl 
eth0      Link encap:Ethernet  HWaddr 02:42:ac:11:00:3c  
          inet addr:172.17.0.60  Bcast:0.0.0.0  Mask:255.255.0.0
          inet6 addr: fe80::42:acff:fe11:3c/64 Scope:Link
          UP BROADCAST  MTU:1500  Metric:1
          RX packets:2 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:168 (168.0 B)  TX bytes:180 (180.0 B)

URL: http://172.17.0.60:5555/
USERNAME: ...
PASSWORD: ...
 * Running on http://0.0.0.0:5555/
...
```

### Advanced
Run PyMPL Web App in background:

```bash
user@locahost ~$ CID=$(docker run -d -p 5555 fdabrandao/pympl)
user@locahost ~$ docker inspect --format URL:http://{{.NetworkSettings.IPAddress}}:5555/ $CID
URL:http://172.17.0.71:5555/
```

List all running PyMPL containers:

```bash
user@locahost ~$ docker ps | grep fdabrandao/pympl
...
```

List URLs of all running PyMPL containers:

```bash
user@locahost ~$ CIDs=$(docker ps | grep fdabrandao/pympl | cut -d" " -f1)
user@locahost ~$ docker inspect --format URL:http://{{.NetworkSettings.IPAddress}}:5555/ $CIDs
...
```

Stop and remove all PyMPL containers:

```bash
user@locahost ~$ docker stop $(docker ps -a | grep fdabrandao/pympl | cut -d" " -f1)
user@locahost ~$ docker rm $(docker ps -a | grep fdabrandao/pympl | cut -d" " -f1)
```

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]