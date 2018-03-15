#!/bin/bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
default_include_dir="$root_dir/ext/libstorj/src"

LIBSTORJ_INCLUDE=${LIBSTORJ_INCLUDE:-$default_include_dir}
echo "\$LIBSTORJ_INCLUDE: ${LIBSTORJ_INCLUDE}"

# if a virtualenv is available, use it
if [ -d "./env" ]; then
    . ./env/bin/activate;
fi

# generate wrapper code from swig interface file
swig -c++ -python -I"$libstorj_include_dir" -outdir lib/ext ./lib/ext/python_libstorj.i && \

# build extension module
python ./setup.py build_ext
