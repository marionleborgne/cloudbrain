#!/bin/bash
#
# This is used to start/stop pipeline

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."
RETVAL=0

start () {
    rm $BASEDIR/src/pipeline/*.pyc
    /usr/bin/env python $BASEDIR/src/pipeline/pipeline-agent.py start
        RETVAL=$?
        if [[ $RETVAL -eq 0 ]]; then
            echo "started pipeline-agent"
        else
            echo "failed to start pipeline-agent"
        fi
        return $RETVAL
}

stop () {
    # TODO: write a real kill script
    ps aux | grep 'pipeline-agent.py start' | grep -v grep | awk '{print $2 }' | xargs sudo kill -9
    /usr/bin/env python $BASEDIR/src/pipeline/pipeline-agent.py stop
        RETVAL=$?
        if [[ $RETVAL -eq 0 ]]; then
            echo "stopped pipeline-agent"
        else
            echo "failed to stop pipeline-agent"
        fi
        return $RETVAL
}

run () {
    echo "running pipeline"
    /usr/bin/env python $BASEDIR/src/pipeline/pipeline-agent.py run
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
