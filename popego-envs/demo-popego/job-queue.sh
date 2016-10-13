#!/bin/bash

# cd to environment root
echo $0
echo `dirname $0`
cd `dirname $0`
echo `pwd`
CONFIG=variables.sh
if [ -r $CONFIG ] ; then
    . $CONFIG
else
    echo "Falta variables.sh";
    exit 1;
fi

export POPEGO_CONF=`pwd`/popserver.ini

do_start() 
{
    if [[ ! -d $PID_DIR ]]; then
        mkdir -p $PID_DIR
        chown $AS_USER $PID_DIR
    fi

    # cargar entorno
    source $PYTHON_ENV/bin/activate

    echo "Starting Consumers..."
    twistd -y consumer.tac -l "$LOG_DIR/consumer.log" \
	--pidfile "$PID_DIR/consumer.pid"

    echo "Starting Queue Service"
    twistd -y queue.tac -l "$LOG_DIR/queue.log" \
	--pidfile "$PID_DIR/queue.pid"
}

do_stop()
{
    if (test -a "$PID_DIR/consumer.pid"); then \
	echo "Stopping Consumer Server"
	kill `cat $PID_DIR/consumer.pid`
    else 
	echo "Consumer Server is not running"
    fi

    if (test -a "$PID_DIR/queue.pid"); then \
	echo "Stopping Queue Server"
	kill `cat $PID_DIR/queue.pid`
    else 
	echo "Queue Server is not running"
    fi
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
