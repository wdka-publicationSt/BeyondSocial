#!/bin/sh

DIR="/var/www/beyond-social.org/html/wiki/images/"
TEST_DIR="images"

IMGS=`find $DIR -type f -iregex ".*\.\(jpg\|jpeg\|png\|gif\)"`

for img in $IMGS;
do mogrify -resize 600x\> $img 
done

php5 /var/www/beyond-social.org/html/wiki/maintenance/refreshImageMetadata.php
