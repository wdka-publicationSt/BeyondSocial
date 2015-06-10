#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib, shlex
from urlparse import urlparse
from urllib import unquote
wd = '/var/www/beyond-social.org/html'

####
# chmod a+w -R index.html articles/ #so that files can be overwritten
####
def update():
   cmd = 'python {}/bs_wiki2web.py'.format(wd)
   subprocess.call(cmd, shell=True)


method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   update()
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   # JSON response
   result = {'success':'true', 'msg':"update is taking place"}   
   print "Content-type: application/json\n\n"
   print json.dumps(result)




