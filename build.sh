#!/bin/bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
libstorj_dir="$root_dir/ext/libstorj/src"

# lame argument parsing
if [ $# -gt 0 ]; then
    libstorj_dir=$1
fi

# if a virtualenv is available, use it
if [ -d "./env" ]; then
    . ./env/bin/activate;
fi

# generate wrapper code from swig interface file
swig -c++ -python -I$libstorj_dir -outdir lib/ext ./lib/ext/python_libstorj.i && \

# build extension module
python ./setup.py build_ext
