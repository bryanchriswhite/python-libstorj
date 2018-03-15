#!/bin/bash

root_dir="/root"

#redis
service redis-server start

#mongodb
service mongod start

#storjbridge
pm2 start -n bridge $root_dir/bin/storj-bridge -- -c $root_dir/config/storj-bridge/config.json -d $root_dir/config/storj-bridge

#wait for things to come up
echo "Sleeping for 5..."
sleep 5