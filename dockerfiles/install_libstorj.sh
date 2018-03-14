#!/bin/bash

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
libstorj_dir="$root_dir/libstorj"

git clone https://github.com/storj/libstorj $libstorj_dir
cd $libstorj_dir && \
./autogen.sh && \
./configure && \
make && \
if [ $(whoami) == "root" ]; then
    make install
    ldconfig
else
    sudo make install
    sudo ldconfig
fi
