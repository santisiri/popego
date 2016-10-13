#!/bin/bash

# cd to environment root
cd `dirname $0`
CONFIG=variables.sh
if [ -r $CONFIG ] ; then
    . $CONFIG
else
    echo "Falta variables.sh";
    exit 1;
fi

export PYTHONHOME=$PYTHON_ENV
export PYTHONPATH=$PYTHON_ENV/lib/python2.5/site-packages
export POPEGO_CONF=`pwd`/popserver.ini

. /lib/lsb/init-functions

do_start() 
{
    if [[ ! -d $PID_DIR ]]; then
        mkdir -p $PID_DIR
	chown $AS_USER $PID_DIR
    fi

    for ((i=0;i<NUMBER_OF_BACKENDS;i++)); do
	start-stop-daemon --background --make-pidfile \
	    --pidfile $PID_DIR/popserver.$((PORTBASE+i)).pid \
	    --exec $AJP_DAEMON --chuid $AS_USER --start -- \
	    -p $((PORTBASE+i)) \
	    -l $LOG_DIR/popserver.$((PORTBASE+i)).log \
	    popserver.wsgi application;

	echo "Started server in port $((PORTBASE+i)) with PID " \
	    `cat $PID_DIR/popserver.$((PORTBASE+i)).pid`;
    done
}

do_stop() 
{
    for ((i=0;i<NUMBER_OF_BACKENDS;i++)); do
	echo "Stopping server with PID " \
	    `cat $PID_DIR/popserver.$((PORTBASE+i)).pid`;

	start-stop-daemon --stop \
	    --pidfile $PID_DIR/popserver.$((PORTBASE+i)).pid;
    done
}

case "$1" in
  start)
  do_start
  ;;
  restart|reload|force-reload)
  do_stop
  sleep 3
  do_start
  ;;
  stop)
  do_stop
  ;;
  *)
  echo "Usage: $0 start|stop|restart" >&2
  exit 3
  ;;
esac
