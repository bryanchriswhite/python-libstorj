`python_libstorj`
===
[![Build Status](https://travis-ci.org/Storj/python-libstorj.svg?branch=master)](https://travis-ci.org/Storj/python-libstorj)

Dependencies
---
+ python 2.7
+ [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
+ [swig](http://www.swig.org/)

Enviroment Setup
---

### Using Docker
1. Clone python_libstorj
    ```
    git clone https://github.com/Storj/python-libstorj
    ```
1. [Create a config file](#configuration)
1. Build the docker image
    ```
    docker build --tag python_libstorj .
    ```
1. Running the container
    ```
    docker run -it \
        -v $(pwd)/lib:/python_libstorj/lib \
        -v $(pwd)/tests:/python_libstorj/tests \
        python_libstorj
    ```

### Using Virtualenv
1. Clone python_libstorj
    ```
    git clone https://github.com/Storj/python-libstorj
    ```
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

Configuration
---
1. Copy `tests/options_example.yml` to `tests/options.yml` and edit:
      + `bridge_options`
        - `user`
        - `pass`
        - `host` _(if applicable)_
        - `port` _(if applicable)_
        - `proto` _(if applicable)_
      + `encrypt_options`
        - `mnemonic`

Running Tests
---
```
python -m unittest discover
```
