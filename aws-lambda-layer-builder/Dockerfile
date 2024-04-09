FROM amazonlinux:2.0.20230307.0

RUN ulimit -n 1024 && yum -y update && yum -y install \
    python37 \
    python3-pip \
    python37-devel \
    zip \
    && yum clean all

RUN python3 -m pip install pip==23.2.1
RUN pip install virtualenv==20.25.0