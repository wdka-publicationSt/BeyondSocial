#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib, shlex
from urlparse import urlparse


def create_preview(filename):
   create = shlex.split('/usr/bin/python ./bs_wiki2web.py --preview Lexicon' )
   touch = shlex.split('/usr/bin/python ./test-touch.py' )
   # shlex.split('touch ../preview/yyyyy')
   p = subprocess.Popen(create, stdout=subprocess.PIPE)
   

method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
   create_preview(wikipage)
   # JSON response
   result = {'success':'true', 'msg':wikipage + " was posted by you"}
   print "Content-type: application/json\n\n"
   print json.dumps(result)
   
#create_preview('Friction_as_a_Formula')




      



