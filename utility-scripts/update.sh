#! /bin/bash
cd /var/www/beyond-social.org/html/beyond-social/
./edit_index.py|./create_article.py |./parse_article_html.py
cp ./*.html ../ 
for i in {./articles,./img,./js,./styles}; do cp $i ../ -r; done
