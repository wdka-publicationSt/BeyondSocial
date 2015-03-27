#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib
from urlparse import urlparse


def create_preview(filename):
   create = 'python /home/andre/Documents/WdKA/BeyondSocial/development/preview_article.py {}'.format(filename)
   subprocess.call(create, shell=True) # saved in tmp_content.html html   
#   return (preview_url)


method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
   create_preview(wikipage)
   #   prev_url = 
   
   # # JSON response
   # result = {'file':filename, 'url':preview_url}
   # print "Content-type: application/json\n\n"
   # print json.dumps(result)
   

      



