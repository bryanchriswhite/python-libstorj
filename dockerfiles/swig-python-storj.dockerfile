FROM ubuntu:16.04

# install build tools, development/build dependencies, and some dev tools
RUN apt update -qq
RUN apt install -yqq build-essential libtool autotools-dev automake libuv1-dev libmicrohttpd-dev bsdmainutils libcurl4-gnutls-dev libjson-c-dev nettle-dev curl
RUN apt install -yqq swig git python-pip
RUN apt install -yqq vim gdb

RUN mkdir -p /setup_libstorj
COPY ./dockerfiles/install_libstorj.sh /setup_libstorj/
RUN chmod 655 /setup_libstorj/*.sh
RUN /setup_libstorj/install_libstorj.sh /setup_libstorj/libstorj
