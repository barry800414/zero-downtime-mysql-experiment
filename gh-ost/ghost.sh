#!/bin/bash

docker run --network mysql-cluster -i -t bonty/gh-ost:latest \
--host="follower.io" \
--port="3306" \
--initially-drop-ghost-table \
--max-load=Threads_running=25 \
--critical-load=Threads_running=1000 \
--chunk-size=1000 \
--max-lag-millis=1500 \
--user="user" \
--password="0000" \
--database="demo" \
--table="qganalyzedata_account" \
--verbose \
--alter="ADD COLUMN demo_field2 varchar(64)" \
--switch-to-rbr \
--allow-master-master \
--cut-over=default \
--exact-rowcount \
--concurrent-rowcount \
--default-retries=120 \
--panic-flag-file=/tmp/ghost.panic.flag \
--postpone-cut-over-flag-file=/tmp/ghost.postpone.flag \
--assume-master-host="leader.io:3306" \
--execute
