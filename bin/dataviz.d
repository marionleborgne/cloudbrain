#!/bin/bash
#
# This is used to start/stop dataviz

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
RETVAL=0

start () {
    /usr/bin/env nodejs $BASEDIR/src/dataviz/server.js &
        RETVAL=$?
        if [[ $RETVAL -eq 0 ]]; then
            echo "started dataviz-agent"
        else
            echo "failed to start dataviz-agent"
        fi
        return $RETVAL
}

stop () {
    # TODO: write a real kill script
    ps aux | grep 'nodejs' | grep -v grep | awk '{print $2 }' | xargs sudo kill -9
        RETVAL=$?
        if [[ $RETVAL -eq 0 ]]; then
            echo "stopped dataviz-agent"
        else
            echo "failed to stop dataviz-agent"
        fi
        return $RETVAL
}

run () {
    echo "running dataviz"
    /usr/bin/env nodejs $BASEDIR/src/dataviz/server.js
}

# See how we were called.
case "$1" in
  start)
    start
        ;;
  stop)
    stop
        ;;
  run)
    run
        ;;
  restart)
    stop
    start
       ;;
  *)
        echo $"Usage: $0 {start|stop|run}"
        exit 2
        ;;
esac
