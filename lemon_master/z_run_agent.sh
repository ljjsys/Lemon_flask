#!/usr/bin/env bash
# created by CountryRoad 2016

python_path=/opt/python-3.5.1/bin
agent_path=/opt/data_sync/data_sync_agent

case "$1" in
    start)
        # run master server, defalt port 59120       ^M
        echo "starting agent server..."
        $python_path/python3 $agent_path/backup_agent.py >> $agent_path/logs/backup_agent.log 2>&1  &
    ;;

    stop)
        echo "info: $0 stop success"
        process="$python_path/python3 $agent_path/backup_agent.py"
        kill $(ps -ef|grep "$process"|grep -v grep|awk '{ print $2 }')
    ;;

    *)

    echo "usage: $0 {start|stop}"
    exit 1
esac
exit 0
