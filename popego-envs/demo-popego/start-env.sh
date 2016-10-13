#!/bin/bash

actualdir=`pwd`
cd `dirname $0`
. variables.sh

export POPEGO_CONF="`pwd`/popserver.ini"
cat > rcfile <<EOF
source /etc/bash.bashrc
source ~/.bashrc
source "$PYTHON_ENV/bin/activate"
export POPEGO_CONF
cd $actualdir
EOF

bash --rcfile rcfile
cd `dirname $0`
rm -f rcfile
