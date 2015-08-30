FROM fdabrandao/vpsolver

USER root
RUN mkdir -p /pympl
ADD . /pympl
ENV HOME=/pympl
WORKDIR /pympl

RUN bash test.sh quick_test

RUN bash install.sh
RUN bash test.sh test_install quick_test

RUN bash install3.sh
RUN bash test3.sh test_install quick_test

CMD bash
