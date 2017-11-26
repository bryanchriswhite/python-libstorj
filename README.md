`python_libstorj`
===
[![Build Status](https://travis-ci.org/Storj/python-libstorj.svg?branch=master)](https://travis-ci.org/Storj/python-libstorj)

Dependencies
---
+ python 2.7
+ [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
+ [swig](http://www.swig.org/)


Environment Setup
---
1. Setup a virtualenv
    ```
    virtualenv env
    ```
1. Activate your virtualenv
    ```
    . env/bin/activate
    ```
1. Copy `tests/options_example.yml` to `tests/options.yml` and edit:
      + `bridge_options`
        - `user`
        - `pass`
        - `host` _(if applicable)_
        - `port` _(if applicable)_
        - `proto` _(if applicable)_
      + `encrypt_options`
        - `mnemonic`

Build
---
Run the build shell script:
```
./build.sh
```

Running Tests
---
```
python -m unittest discover
```
