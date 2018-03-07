#!/bin/bash

if [ -d "./env" ]; then
    . ./env/bin/activate;
fi
swig -c++ -python -outdir lib/ext ./lib/ext/python_libstorj.i && \
python ./setup.py build_ext
