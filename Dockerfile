FROM halotools/python-sdk:ubuntu-16.04_sdk-1.0.4_2018-01-22
MAINTAINER toolbox@cloudpassage.com

RUN apt-get update -y && \
    apt-get install -y \
    systemd=229-4ubuntu21.2 \
    sensible-utils=0.0.9ubuntu0.16.04.1 \
    isc-dhcp-client=4.3.3-5ubuntu12.9 \
    libssl1.0.0:amd64=1.0.2g-1ubuntu4.12

RUN mkdir /vulnerable_image_check

COPY runner.py /

COPY vulnerable_image_check/ /vulnerable_image_check/

WORKDIR /

CMD ["/usr/bin/python", "runner.py"]
