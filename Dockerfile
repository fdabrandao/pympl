FROM fdabrandao/vpsolver

USER root
RUN mkdir -p /pympl
ADD . /pympl
ENV HOME=/pympl
WORKDIR /pympl

RUN DEBIAN_FRONTEND=noninteractive bash install.sh
RUN DEBIAN_FRONTEND=noninteractive bash test.sh test_install quick_test

RUN DEBIAN_FRONTEND=noninteractive apt-get install python3-setuptools
RUN DEBIAN_FRONTEND=noninteractive sudo easy_install3 pip
RUN DEBIAN_FRONTEND=noninteractive bash install.sh
RUN DEBIAN_FRONTEND=noninteractive mv /usr/local/bin/pip2 /usr/local/bin/pip
RUN DEBIAN_FRONTEND=noninteractive bash test3.sh test_install quick_test

CMD bash
