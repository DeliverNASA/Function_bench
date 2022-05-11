FROM ubuntu
WORKDIR /usr/local
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install libjpeg8 libimagequant0 libtiff5 libgl1 libglib2.0-dev
CMD [ "/bin/bash" ]