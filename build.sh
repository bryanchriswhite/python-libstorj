#!/bin/bash

. ./env/bin/activate;
swig -c++ -python ./python_libstorj.i && \
python ./setup.py build_ext --inplace
