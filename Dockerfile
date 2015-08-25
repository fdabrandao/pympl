FROM fdabrandao/vpsolver

USER root
RUN mkdir -p /pympl
ADD . /pympl
ENV HOME=/pympl
WORKDIR /pympl

RUN DEBIAN_FRONTEND=noninteractive bash install.sh
RUN DEBIAN_FRONTEND=noninteractive bash test.sh test_install quick_test

CMD bash
