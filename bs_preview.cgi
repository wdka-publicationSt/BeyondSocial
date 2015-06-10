#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib, shlex
from urlparse import urlparse
from urllib import unquote
wd = '/var/www/beyond-social.org/html'

def create_preview(filename):
   cmd = 'python {}/bs_wiki2web.py --preview "{}"'.format(wd, filename)
   subprocess.call(cmd, shell=True)


method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
   wikipage=unquote(wikipage)
   # JSON response
   result = {'success':'true', 'msg':wikipage + " was posted by you."}   
   print "Content-type: application/json\n\n"
   print json.dumps(result)
   create_preview(wikipage) #def w/ subprocess can only come after posting

