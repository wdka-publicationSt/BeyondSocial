#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib, shlex
from urlparse import urlparse


## bug:
## before hand I had to use #!/usr/bin/python2.6
## as to run a python cgi

def create_preview(filename):
   wd = '/home/andre/Documents/WdKA/BeyondSocial/development'
   cmd = 'python {}/bs_wiki2web.py --preview Lexicon'.format(wd)
   #create = shlex.split( cmd )
   #touch = shlex.split('/usr/bin/python ./test-touch.py' )#works fine
   # shlex.split('touch ../preview/yyyyy')
   subprocess.call(cmd, shell=True)


method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
   create_preview(wikipage)
   # JSON response
   result = {'success':'true', 'msg':wikipage + " was posted by you"}
   print "Content-type: application/json\n\n"
   print json.dumps(result)
   
create_preview('Lexicon')




      



