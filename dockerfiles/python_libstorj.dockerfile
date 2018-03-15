FROM storjlabs/storj-integration:swig-python-libstorj

# make working directory
RUN mkdir /python_libstorj

# copy scripts and source
COPY ./dockerfiles/install_libstorj.sh ./build.sh ./requirements.txt ./setup.py ./setup.cfg /python_libstorj/
COPY ./dockerfiles/setup_user /python_libstorj/setup_user
COPY ./lib /python_libstorj/lib
COPY ./tests /python_libstorj/tests

# modify file permissions
ls /python_libstorj/setup-user
RUN chmod 655 /python_libstorj/setup-user/{*.{js,sh}}
WORKDIR /python_libstorj/setup_user

# setup env variables
ARG STORJ_EMAIL=''
ARG STORJ_PASS=''
ARG STORJ_KEYPASS=''
ARG STORJ_MNEMONIC=''
ENV STORJ_EMAIL=$STORJ_EMAIL
ENV STORJ_KEYPASS=$STORJ_KEYPASS
ENV STORJ_PASS=$STORJ_PASS
ENV STORJ_MNEMONIC=$STORJ_MNEMONIC
ENV STORJ_BRIDGE='http://127.0.0.1:6382'

RUN . /root/.nvm/nvm.sh \
    && npm install \
    && ./start_bridge.sh \
    && ./create_user.sh \
    && ./activate_user.js \
    && ./import_keys.sh

# useful if you want to interact with mongo from
# a "linked" container (e.g. python_libstorj)
# or from your host (if using just docker - don't forget `-p`)
EXPOSE 27017

# install python dependencies and build python_libstorj
WORKDIR /python_libstorj
RUN pip install -r ./requirements.txt
RUN ./build.sh

# setup env variables
# (uncomment/modify for use outside of docker-compose)
#ARG STORJ_BRIDGE='https://api.storj.io'
#ARG STORJ_KEYPASS=''
#ENV STORJ_BRIDGE=$STORJ_BRIDGE
#ENV STORJ_KEYPASS=$STORJ_KEYPASS

CMD /bin/bash