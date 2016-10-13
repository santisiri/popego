#!/bin/bash

pid_dir=/var/run/clean-popego
log_dir=/var/log/clean-popego
path=/home/popego/clean-popego/branches/widget-revenge/jq

# cd to project root
cd $path

# cargar entorno
source /usr/local/pythonenv/CLEAN-POPEGO/bin/activate

echo "Starting Consumers..."
twistd -y "$path/jq/tacs/clean-popego-consumer.tac" -l "$log_dir/consumer.log" --pidfile "$pid_dir/consumer.pid"

echo "Starting Queue Service"
twistd -y "$path/jq/tacs/clean-popego-queue.tac" -l "$log_dir/queue.log" --pidfile "$pid_dir/queue.pid"
