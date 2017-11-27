#!/bin/bash

deps_dir=$HOME/dependencies
mkdir -p $deps_dir
git clone https://github.com/bryanchriswhite/libstorj $deps_dir/libstorj
curl -o $deps_dir/nettle-3.4.tar.gz https://ftp.gnu.org/gnu/nettle/nettle-3.4.tar.gz
curl -Lo $deps_dir/libuv-1.8.0.tar.gz https://github.com/libuv/libuv/archive/v1.8.0.tar.gz
echo "ls $deps_dir"
ls $deps_dir

cd $deps_dir
echo "tar -xzf $deps_dir/nettle-3.4.tar.gz"
tar -xzf $deps_dir/nettle-3.4.tar.gz
echo "tar -xzf $deps_dir/libuv-1.8.0.tar.gz"
tar -xzf $deps_dir/libuv-1.8.0.tar.gz

echo "ls $deps_dir"
ls $deps_dir

cd $deps_dir/nettle-3.4
./configure
make
sudo make install

cd $deps_dir/libuv-1.8.0
sh ./autogen.sh
CFLAGS="-std=c99" ./configure
#./configure
make
sudo make install
sudo make install-includeHEADERS

cd $deps_dir/libstorj
./autogen.sh
CFLAGS="-std=c99" ./configure
#./configure
make
sudo make install

