`python_libstorj`
=================
[![Storj.io](https://storj.io/img/storj-badge.svg)](https://storj.io)
[![Build Status](https://travis-ci.org/Storj/python-libstorj.svg?branch=master)](https://travis-ci.org/Storj/python-libstorj)
[![Chat on rocket.chat](https://img.shields.io/badge/chat-rocket.chat-red.svg)](https://community.storj.io/channel/dev)

Dependencies
---
+ python 2.7
+ [swig](http://www.swig.org/)
+ [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) _(optional)_
+ [docker](https://docs.docker.com/) _(optional)_

Enviroment Setup
---
This section aims to explain how to get multiple environments setup and working with `python_libstorj`.
These different environments aren't necessarily mutually exclusive; you can choose how you would like to interact with `python_libstorj`.

### (Common Steps)
* #### Clone python_libstorj
    ```
    git clone https://github.com/Storj/python-libstorj
    ```
* #### Configuration
    The [`tests/`](./tests/) directory contains multiple example "`options.yml`" files.
    Depending on which environment you choose, you may want to use the respective example file.
    Copy `tests/options.<some>_example.yml` to `tests/options.yml` and edit:
    + `bridge_options`
      - `user`
      - `pass`
      - `host` _(if applicable)_
      - `port` _(if applicable)_
      - `proto` _(if applicable)_
    + `encrypt_options`
      - `mnemonic`

    _See [`libstorj`](https://github.com/storj/libstorj#libstorj) for an easy way to create/import/export users/mnemonics (`libstorj --help`)._


### Using Docker
Using docker is a convenient way to get into a completely ready to go environment.
The image is based on [`storjlabs/storj-integration`](https://github.com/Storj/integration) image which runs a complete mini storj backend:

_Bridge (1x), Bridge-monitor(1x), Renters (6x), Farmers (16x)_

You can use the [`python_libstorj.dockerfile`](./dockerfiles/python_libstorj.dockerfile) as a starting point for building a custom docker environment with `python_libstorj` installed **and** built from source.
This is ideal for use as a development environment for `python_libstorj`, for example.

The [`libstorj`](https://github.com/storj/libstorj#libstorj) cli tool is already installed in the `python_libstorj` image; it's used to **automatically** register and activate a user, **during `docker build`**, with the credentials provided in the following build-args and/or environment variables:

  ```
  # See https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg


  STORJ_EMAIL    # email address of storj user
  STORJ_PASS     # basicauth password of storj user
  STORJ_KEYPASS  # cli credential encryption passphrase
  STORJ_MNEMONIC # mnemonic of a storj user
  STORJ_BRIDGE   # the bridge server to talk to (e.g.  https://api.storj.io)
                 #   - defaults to http://127.0.0.1:6382
  ```

See the help for more info (`libstorj --help`).

1. [Clone python_libstorj](#clone-python_libstorj)

1. [Create a config file](#configuration)

    The [`options.docker_example.yml`](./tests/options.docker_example.yml) only requires changes to the `user`, `pass` and `mnemonic` properties; further changes are optional.

1. Build the python_libstorj image

    ```
    # See https://docs.docker.com/engine/reference/commandline/build/

    docker build --tag python_libstorj \
        --build-arg STORJ_EMAIL="<email>" \
        --build-arg STORJ_PASS="<password>" \
        --build-arg STORJ_MNEMONIC="<mnemonic>" \
        -f ./dockerfiles/python_libstorj.dockerfile .

    # optionally add the `--no-cache` arg to ensure a fresh build
    ```

    Note: `STORJ_BRIDGE` and `STORJ_KEYPASS` environment variables (and corresponding build-args; see [`libstorj`](https://github.com/storj/libstorj) for more info - _(these currently only apply to the `libstorj` cli (i.e. `options.yml` is used by the unittest suite))_.

1. Run/Create/Start a `python_libstorj` container

    ```
    # See https://docs.docker.com/engine/reference/commandline/run/
    #     https://docs.docker.com/engine/reference/commandline/create/
    #     https://docs.docker.com/engine/reference/commandline/start/

    # See volumes: https://docs.docker.com/storage/volumes/
    # use of volumes (i.e. `-v`) is optional

    # Get a quick shell in a `python_libstorj` container
    docker run -v $(pwd)/tests:/python_libstorj/tests \
               -v $(pwd)/lib:/python_libstorj/lib \
               -it --name python_libstorj_1 python_libstorj

    # Get an ephemeral container
    docker run --rm -it python_libstorj

    # Create (but don't start) a persistent container
    docker create -v $(pwd)/tests:/python_libstorj/tests \
                  -v $(pwd)/lib:/python_libstorj/lib \
                  -it --name python_libstorj_1 python_libstorj

    # Start a stopped container
    # (either from a previous `create` or `run`)
    docker start -ai python_libstorj_1

    # Deleting a container
    # If you used the `--name` arg you will need to delete
    # the container with that name before you can re-create it
    docker rm python_libstorj_1 # following the example above

    #   You can use `docker ps` to see what containers are running.
    ```

### Using [Docker](https://www.docker.com/what-docker)
1. [Clone python_libstorj](#clone-python_libstorj)
1. [Create a config file](#configuration)
1. Build the docker image
    ```
    # See https://docs.docker.com/engine/reference/commandline/build/

    docker build --tag python_libstorj -f ./dockerfiles/python_libstorj.dockerfile .
    ```
1. Running the container
    ```
    # See https://docs.docker.com/engine/reference/run/
    #     https://docs.docker.com/engine/reference/run/#volume-shared-filesystems

    docker run -it \
        -v $(pwd)/lib:/python_libstorj/lib \
        -v $(pwd)/tests:/python_libstorj/tests \
        python_libstorj
    ```

1. Start a local storj backend _(optional)_

    From within the `python_libstorj` container:
    ```
    # See https://github.com/storj/libstorj
    /root/scripts/start_everything.sh
    ```


### Using [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
1. [Clone python_libstorj](#clone-python_libstorj)
1. Setup a virtualenv
    ```
    virtualenv env
    ```
1. Activate your virtualenv
    ```
    . env/bin/activate
    ```
1. Install pip dependencies
    ```
    pip install -r ./requirements.txt
    ```
1. [Create a config file](#configuration)

Build
---
Run the build shell script:
```
./build.sh
```

Building needs to be done once initially (already done if you're using docker), and any time changes are made to C/C++ and/or swig interface source (e.g. `./lib/*.{cpp,h,i}`)

Running Tests
---
```
python -m unittest discover
```
