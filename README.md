`python_libstorj`
===
[![Build Status](https://travis-ci.org/Storj/python-libstorj.svg?branch=master)](https://travis-ci.org/Storj/python-libstorj)

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

You can use the [`Dockerfile`](./Dockerfile) as a starting point for building a custom docker environment with `python_libstorj` installed *and* built from source.
This is ideal for use as a development environment for `python_libstorj`, for example.

1. [Clone python_libstorj](#clone-python_libstorj)

1. [Create a config file](#configuration)

    The [`options.docker_example.yml`](./tests/options.docker_example.yml) only requires changes to the `user`, `pass` and `mnemonic` properties; further changes are optional.
    The [`libstorj`](https://github.com/storj/libstorj#libstorj) cli tool is already installed in the `python_libstorj` service's image; see the help for more info (`libstorj --help`).
1. Build the python_libstorj service _(optional)_

    ```
    # See https://docs.docker.com/compose/reference/

    docker-compose build
    # docker-compose build --no-cache #ensures fresh build
    ```
1. Edit `docker-compose.yml` _(optional)_

    Have a look at:
    [ [`environment`](https://docs.docker.com/compose/compose-file/compose-file-v2/#environment) | [`volumes`](https://docs.docker.com/compose/compose-file/compose-file-v2/#volume-configuration-reference) | [`command`](https://docs.docker.com/compose/compose-file/compose-file-v2/#command) | [`links`](https://docs.docker.com/compose/compose-file/compose-file-v2/#links) | [`ports`](https://docs.docker.com/compose/compose-file/compose-file-v2/#ports) ]

    Note: `STORJ_BRIDGE` and `STORJ_KEYPASS` environment variables; see [`libstorj`](https://github.com/storj/libstorj) for more info - _(these currently only apply to the `libstorj` cli)_.

1. Run `python_libstorj`
    ```
    # See https://docs.docker.com/compose/reference/

    # Get a shell in a `python_libstorj` container
    docker-compose run python_libstorj

    #   Because the composition `links` the `bridge` service, docker-compose
    #   should ensure that `bridge` is running and port-forwarded for use
    #   within the `python_libstorj` service.
    #
    #   You can use `docker-compose ps` to see what services are running.
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
