#!/bin/bash
if [ ! $VIRTUAL_ENV ]
then
    echo 'No virtual environment defined. Refusing to run.'
    exit 1
fi

if [ ! $1 ]
then
    echo "Usage: $0 path_to_ini_file"
    exit 1
fi

# `dirname $0` is the 'scripts' directory
APP_ROOT="`dirname $0`/.."

echo 'setting maintenance page'
cp $APP_ROOT/../webtemplates/maintenance.html $APP_ROOT/popserver/public/maintenance.html

echo 'removing static assets'
rm -rf $APP_ROOT/popserver/public/javascripts $APP_ROOT/popserver/public/css

echo 'updating to latest revision'
svn up $APP_ROOT/..

echo 'compressing js and css'
$APP_ROOT/scripts/compress_assets.sh

# get current revision
DEPLOYED_REVISION=`svn info $APP_ROOT/popserver | grep Revision | awk '{print $2}'`

#echo 'creating stylesheet bundle'
#python $APP_ROOT/scripts/bundle_stylesheets.py $1 > $APP_ROOT/popserver/public/css/popego_style_$DEPLOYED_REVISION.css

echo 'running schema and data migrations'
python $APP_ROOT/scripts/migrate.py $1 -v
python $APP_ROOT/scripts/data_migrate.py $1 -v

echo 'restarting JQueue'
/etc/init.d/alpha-popego-queue restart

echo 'creating revision info file'
echo "Currently deployed revision: $DEPLOYED_REVISION" > $APP_ROOT/popserver/public/revision.txt

echo 'removing maintenance page'
rm $APP_ROOT/popserver/public/maintenance.html

# el usuario `popego` puede ejecutar `sudo /etc/init.d/apache2` sin password (ver /etc/sudoers)
echo 'restarting apache'
sudo /etc/init.d/apache2 force-reload
