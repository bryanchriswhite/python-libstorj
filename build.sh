#!/bin/bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# if a virtualenv is available, use it
if [ -d "./env" ]; then
    . ./env/bin/activate;
fi

# lame argument parsing
output_dir=lib/ext
interface_file=./lib/ext/python_libstorj.i
if [ $# -gt 0 ]; then
  output_dir=$1
fi
if [ $# -gt 1 ]; then
  output_dir=$2
fi

# generate wrapper code from swig interface file
cd $root_dir && swig -c++ -python -outdir $output_dir $interface_file && \

# build extension module
python ./setup.py build_ext
