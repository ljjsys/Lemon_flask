#!/usr/bin/env bash

# created by CountryRoad 2015

python_path=/opt/python-3.5.1/bin
master_path=/opt/data_sync/data_sync_master

case "$1" in
    start)
        # run master WEB-UI, default port 12000
        $python_path/python3  $master_path/web_UI.py >> $master_path/logs/lemon_master_webui.log 2>&1  &
        echo "starting web_UI server..."
    ;;

    stop)
        process="$python_path/python3 $master_path/web_UI.py"
        kill $(ps -ef|grep "$process"|grep -v grep|awk '{ print $2 }')
        echo $"info: $0 stop success"
    ;;

    *)

    echo "usage: $0 {start|stop}"
    exit 1
esac
exit 0
