#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib, shlex
from urlparse import urlparse


def create_preview(filename):
   create = shlex.split('/usr/bin/python /var/www/beyond-social.org/html/bs_wiki2web.py --preview "{}"'.format(filename) )
   subprocess.Popen( create, cwd='/var/www/beyond-social.org/html/') # error stdout=subprocess.PIPE, stderr=subprocess.STDOUT # 
#   out, error = p.communicate()
   return create

def touch():
   touch = shlex.split('touch /var/www/beyond-social.org/html/preview/yyyyy')
   p = subprocess.Popen(touch) # saved
   return touch

# out, error = create_preview('Lexicon') #test
# print out, error

method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
#   t = touch()
#   t = " ".join(t)
   p = create_preview(wikipage)
   p = " ".join(p)

  # JSON response
   result = {'success':'true', 'msg':p +" was posted by you"}
   print "Content-type: application/json\n\n"
   print json.dumps(result)
   




      



