#!/bin/bash

# compress javascript and CSS files using yuicompressor

YUI="/home/popego/bin/yuicompressor.jar"
PUBLIC_PATH="/home/popego/alpha.popego.com/current/popserver/public"

# compress stylesheets
find $PUBLIC_PATH -name "*.css" -exec python $PUBLIC_PATH/../../scripts/process_stylesheet.py $PUBLIC_PATH/../../alpha-popego.ini '{}' \; -exec java -jar $YUI --type css -o '{}' '{}' \;

# compress javascript
find $PUBLIC_PATH -name "*.js" -exec java -jar $YUI --preserve-semi --preserve-strings --type js --nomunge -o '{}' '{}' \;
