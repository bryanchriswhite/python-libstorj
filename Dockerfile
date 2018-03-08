FROM ubuntu:16.04
RUN mkdir /python_libstorj
RUN apt update -qq
RUN apt install -yqq build-essential libtool autotools-dev automake libuv1-dev libmicrohttpd-dev bsdmainutils libcurl4-gnutls-dev libjson-c-dev nettle-dev curl
RUN apt install -yqq swig git python-pip
COPY ./install_libstorj.sh ./build.sh ./requirements.txt ./setup.py ./setup.cfg /python_libstorj/
COPY ./lib /python_libstorj/lib
COPY ./tests /python_libstorj/tests
RUN chmod 655 /python_libstorj/install_libstorj.sh
RUN chmod 655 /python_libstorj/build.sh
WORKDIR /python_libstorj
RUN ./install_libstorj.sh
RUN ./build.sh
RUN pip install -r ./requirements.txt
CMD /bin/bash