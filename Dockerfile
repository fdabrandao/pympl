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

EXPOSE 5555
CMD ifconfig eth0 && \
    python -m pympl.webapp.app 5555 `date | md5sum | head -c${1:-8}`
