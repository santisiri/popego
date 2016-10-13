#!/bin/bash
path=`dirname $0`/..

if (test -a "$path/pid/consumer.pid"); then \
  echo "Stopping Consumer Server"
  kill `cat $path/pid/consumer.pid`
else 
  echo "Consumer Server is not running"
fi

if (test -a "$path/pid/queue.pid"); then \
  echo "Stopping Queue Server"
  kill `cat $path/pid/queue.pid`
else 
  echo "Queue Server is not running"
fi
