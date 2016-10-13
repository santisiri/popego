#!/bin/bash

pid_path=/var/run/demo-popego

if (test -a "$pid_path/consumer.pid"); then \
  echo "Stopping Consumer Server"
  kill `cat $pid_path/consumer.pid`
else 
  echo "Consumer Server is not running"
fi

if (test -a "$pid_path/queue.pid"); then \
  echo "Stopping Queue Server"
  kill `cat $pid_path/queue.pid`
else 
  echo "Queue Server is not running"
fi
