FROM fdabrandao/docker-ubuntu

MAINTAINER Filipe Brandão <fdabrandao@dcc.fc.up.pt>

USER root
RUN mkdir -p /pympl
ADD . /pympl
ENV HOME=/pympl
WORKDIR /pympl

RUN pip2 install pyvpsolver --pre
RUN pip3 install pyvpsolver --pre

RUN pip2 install -r requirements.txt
RUN bash test.sh quick_test

RUN bash install.sh
RUN bash test.sh test_install quick_test

RUN bash install3.sh
RUN bash test3.sh test_install quick_test

EXPOSE 5555
CMD ifconfig eth0 && \
    python -m pympl.webapp.app 5555 `date | md5sum | head -c${1:-16}`
