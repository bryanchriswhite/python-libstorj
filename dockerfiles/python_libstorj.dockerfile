FROM storjlabs/storj-integration:swig-python-libstorj

# make working directory
RUN mkdir /python_libstorj

# copy scripts and source
COPY ./build.sh ./requirements.txt ./setup.py /python_libstorj/
COPY ./dockerfiles/setup_user /python_libstorj/setup_user
COPY ./lib /python_libstorj/lib
COPY ./tests /python_libstorj/tests
RUN ls /python_libstorj/tests
RUN cat /python_libstorj/tests/options.yml
RUN storj get-info
RUN storj ls
RUN mkdir -p /python_libstorj/ext
RUN ln -s /libstorj /python_libstorj/ext/libstorj

# modify file permissions
RUN chmod 655 /python_libstorj/setup_user/*.{js,sh}
WORKDIR /python_libstorj/setup_user

# setup env variables
ARG STORJ_EMAIL=''
ARG STORJ_PASS=''
ARG STORJ_KEYPASS=''
ARG STORJ_MNEMONIC=''
ARG STORJ_BRIDGE='http://127.0.0.1:6382'
ARG LIBSTORJ_INCLUDE='/root/libstorj/src'
ENV STORJ_EMAIL=$STORJ_EMAIL
ENV STORJ_KEYPASS=$STORJ_KEYPASS
ENV STORJ_PASS=$STORJ_PASS
ENV STORJ_MNEMONIC=$STORJ_MNEMONIC
ENV STORJ_BRIDGE=$STORJ_BRIDGE
ENV LIBSTORJ_INCLUDE=$LIBSTORJ_INCLUDE

# remove STORJ_BRIDGE export in .bashrc
RUN sed -i '/export STORJ_BRIDGE.*/d' /root/.bashrc
# reduce number of farmers and renters
RUN sed -ri '/pm2 start -n \w+-([^1]|[0-9]{2,})/d' /root/scripts/start_everything.sh
RUN sed -ri 's/totalRenters": \d+/totalRenters": 1/' /root/config/storj-complex/renter-1.json

RUN ./setup_user.sh

# useful if you want to interact with mongo from
# a "linked" container (e.g. python_libstorj)
# or from your host (if using just docker - don't forget `-p`)
EXPOSE 27017

# install python dependencies and build python_libstorj
WORKDIR /python_libstorj
RUN pip install -r ./requirements.txt
RUN ./build.sh

CMD /bin/bash