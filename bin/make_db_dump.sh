#!/bin/bash
DUMP_FILE=~/db_dumps/popego_alpha-`date +%Y%m%d`.sql.bz2
pg_dump -c -h localhost -U popego popego_alpha | bzip2 > $DUMP_FILE
echo "Dump created in $DUMP_FILE"
