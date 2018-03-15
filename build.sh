#!/bin/bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
libstorj_include_dir="$root_dir/ext/libstorj/src"

LIBSTORJ_INCLUDE=$(printenv LIBSTORJ_INCLUDE)
if [ ! -z $LIBSTORJ_INCLUDE ]; then
    libstorj_include_dir=$LIBSTORJ_INCLUDE
fi

# if a virtualenv is available, use it
if [ -d "./env" ]; then
    . ./env/bin/activate;
fi

# generate wrapper code from swig interface file
swig -c++ -python -I"$libstorj_include_dir" -outdir lib/ext ./lib/ext/python_libstorj.i && \

# build extension module
python ./setup.py build_ext
