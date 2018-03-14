FROM storjlabs/swig-python-storj

# make working directory
RUN mkdir /python_libstorj

# copy scripts and source
COPY ./build.sh ./requirements.txt ./setup.py ./setup.cfg /python_libstorj/
COPY ./dockerfiles/setup_user /python_libstorj/setup_user
COPY ./lib /python_libstorj/lib
COPY ./tests /python_libstorj/tests

# modify file permissions
RUN chmod 655 /python_libstorj/{*,setup-user/}.sh
WORKDIR /python_libstorj/setup_user
RUN ./import_keys.sh

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