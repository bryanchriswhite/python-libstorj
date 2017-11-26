#!/bin/bash

LIBSTORJ_DIR = $HOME/libstorj
makedir -p $LIBSTORJ_DIR
git clone https://github.com/storj/libstorj $LIBSTORJ_DIR
cd $LIBSTORJ_DIR
./autogen.sh
./configure
make
sudo make install

