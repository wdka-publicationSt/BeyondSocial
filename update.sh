#! /bin/bash
./edit_index.py|./create_article.py
cp *.html ../ -v
for i in {img,js,styles}; do cp $i ../ -rv; done

