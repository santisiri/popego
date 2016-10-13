#!/bin/bash

path=/home/popego/popego-envs/alpha-popego
. $path/variables.sh
export POPEGO_CONF="$path/popserver.ini"
source "$PYTHON_ENV/bin/activate"

echo "Cron: Update Item All Tags Process starting at `date`" >> $LOG_DIR/cron.log

cd /home/popego/alpha.popego.com/current
python scripts/cron_dispatcher.py item_all_tags > /dev/null 

echo "Cron: Update Item All Tags Process ended at `date`" >> $LOG_DIR/cron.log
