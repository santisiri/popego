#!/bin/bash
path=`dirname $0`/..

echo "Starting Consumers..."
twistd -y "$path/jq/tacs/consumer.tac" -l "$path/log/consumer.log" \
  --pidfile "$path/pid/consumer.pid"

echo "Starting Queue Service en port 8787"
twistd -y "$path/jq/tacs/queue.tac" -l "$path/log/queue.log" \
  --pidfile "$path/pid/queue.pid"
