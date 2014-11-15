#! /bin/bash
./edit_index.py|./create_article.py
cp *.html ../ 
for i in {articles,img,js,styles}; do cp $i ../ -r; done

