#!/bin/bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# if a virtualenv is available, use it
if [ -d "./env" ]; then
    . ./env/bin/activate;
fi

# generate wrapper code from swig interface file
cd $root_dir && swig -c++ -python -outdir lib/ext ./lib/ext/python_libstorj.i && \

# build extension module
python ./setup.py build_ext
