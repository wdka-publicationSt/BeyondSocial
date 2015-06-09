#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, urllib, shlex
from urlparse import urlparse


## bug:
## before hand I had to use #!/usr/bin/python2.6
## as to run a python cgi

def create_preview(filename):
<<<<<<< HEAD:bs_preview.cgi
   wd = '/home/andre/Documents/WdKA/BeyondSocial/development'
   cmd = 'python {}/bs_wiki2web.py --preview Lexicon'.format(wd)
   #create = shlex.split( cmd )
   #touch = shlex.split('/usr/bin/python ./test-touch.py' )#works fine
   # shlex.split('touch ../preview/yyyyy')
   subprocess.call(cmd, shell=True)
=======
   create = shlex.split('/usr/bin/python ./bs_wiki2web.py --preview Lexicon' )
   touch = shlex.split('/usr/bin/python ./test-touch.py' )#works fine
   # shlex.split('touch ../preview/yyyyy')
#   subprocess.call(create)
   p = subprocess.Popen(create, stdout=subprocess.PIPE)
>>>>>>> c88a435404a853cadae264e9170601d2dfa5e7d0:cgi-bin/bs_preview.cgi


method = os.environ.get("REQUEST_METHOD")
if method == "POST":
   myjson =  json.load(sys.stdin) #receive JSON object send from Ajax call
   wikipage=myjson['wikipage'] #in JSON look for value of key 'myquery'
   create_preview(wikipage)
   # JSON response
   result = {'success':'true', 'msg':wikipage + " was posted by you"}
   print "Content-type: application/json\n\n"
   print json.dumps(result)
   
<<<<<<< HEAD:bs_preview.cgi
create_preview('Lexicon')
=======
#create_preview('Friction_as_a_Formula')
>>>>>>> c88a435404a853cadae264e9170601d2dfa5e7d0:cgi-bin/bs_preview.cgi




      



