#/bin/bash

service redis-server stop
service mongod stop
pm2 delete all