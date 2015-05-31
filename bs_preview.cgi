#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib
from urlparse import urlparse


def create_preview(filename):
   create = 'python bs_wiki2web.py --preview "{}"'.format(filename) 
   subprocess.call(create, cwd='/var/www/beyond-social.org/html/', shell=True)

#create_preview('Lexicon') #test

method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
   create_preview(wikipage)
   # JSON response
   result = {'success':'true', 'msg':wikipage + " was posted by you"}
   print "Content-type: application/json\n\n"
   print json.dumps(result)
   




      



