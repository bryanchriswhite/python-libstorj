#!/bin/bash

. ./env/bin/activate;
swig -c++ -python -outdir lib/ext ./lib/ext/python_libstorj.i && \
python ./setup.py build_ext
