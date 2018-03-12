FROM ubuntu:16.04

# make working directory
RUN mkdir /python_libstorj

# install build tools, development/build dependencies, and some dev tools
RUN apt update -qq
RUN apt install -yqq build-essential libtool autotools-dev automake libuv1-dev libmicrohttpd-dev bsdmainutils libcurl4-gnutls-dev libjson-c-dev nettle-dev curl
RUN apt install -yqq swig git python-pip
RUN apt install -yqq vim gdb

# copy scripts and source
COPY ./install_libstorj.sh ./build.sh ./requirements.txt ./setup.py ./setup.cfg /python_libstorj/
COPY ./lib /python_libstorj/lib
COPY ./tests /python_libstorj/tests

# modify file permissions
RUN chmod 655 /python_libstorj/install_libstorj.sh
RUN chmod 655 /python_libstorj/build.sh

# install libstorj, python dependencies, and build python_libstorj
WORKDIR /python_libstorj
RUN ./install_libstorj.sh
RUN pip install -r ./requirements.txt
RUN ./build.sh

# setup env variables
# (uncomment/modify for use outside of docker-compose)
#ARG STORJ_BRIDGE='https://api.storj.io'
#ARG STORJ_KEYPASS=''
#ENV STORJ_BRIDGE=$STORJ_BRIDGE
#ENV STORJ_KEYPASS=$STORJ_KEYPASS

CMD /bin/bash