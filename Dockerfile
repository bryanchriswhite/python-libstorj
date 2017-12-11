FROM ubuntu:16.04
RUN mkdir /python-libstorj
ADD ./install_libstorj.sh /python-libstorj/install_libstorj.sh
#RUN chmod 600 /python-libstorj/install_libstorj.sh
RUN /python_libstorj/install_libstorj.sh
RUN apt update -qq
RUN apt install swig git build-essential libtool autotools-dev automake libmicrohttpd-dev bsdmainutils libcurl4-gnutls-dev libjson-c-dev nettle-dev libuv-dev