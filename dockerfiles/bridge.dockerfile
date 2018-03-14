FROM storjlabs/storj-integration:swig-python-libstorj

COPY ./dockerfiles/setup_user /root/scripts/setup_user

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

RUN chmod 655 /root/scripts/{*.sh,setup_user/*.{sh,js}}
RUN /root/scripts/install_libstorj.sh
WORKDIR /root/scripts/setup_user
RUN . /root/.nvm/nvm.sh \
    && npm install \
    && ./start_bridge.sh \
    && ./create_user.sh \
    && ./activate_user.js \
    && ./import_keys.sh \
    && ../stop_everything.sh

# useful if you want to interact with mongo from
# a "linked" container (e.g. python_libstorj)
# or from your host (if using just docker - don't forget `-p`)
EXPOSE 27017

WORKDIR /root