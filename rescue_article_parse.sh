#!/bin/sh
for i in articles/*.html; do echo $i|sed 's/articles\//''/g'|sed 's/\.html/''/g'|./parse_article_html.py ; done
