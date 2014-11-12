#! /bin/bash
cp *.html ../ -v
for i in {img,js,styles}; do cp $i ../ -rv; done

