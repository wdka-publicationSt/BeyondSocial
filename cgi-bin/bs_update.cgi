#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import cgi, os, json, sys, subprocess, shlex

def update():
   filename = 'update.sh'
   script_path = '/home/andre/Documents/WdKA/BeyondSocial/development/update.sh'
   create = '/bin/bash {}'.format(filename) ## ChHANGE TO CHICHI   
   local = '/home/andre/Documents/WdKA/BeyondSocial/development/'
   chichi = '/var/www/beyond-social.org/html/beyond-social/development'

#   cmd = 'python {}/edit_index.py'.format(local)
   cmd1 = 'cd {}; python edit_index.py'.format(local)
   p1 = subprocess.Popen(cmd1 , shell=True, stdout=subprocess.PIPE)
#   p1_value = p1.communicate()
   cmd2 = 'cd {}; python create_article.py'.format(local)
   p2 = subprocess.Popen(cmd2 , shell=True,  stdin=p1.stdout, stdout=subprocess.PIPE)
   cmd3 = 'cd {}; python parse_article_html.py'.format(local)
   p3 = subprocess.Popen(cmd3 , shell=True,  stdin=p2.stdout, stdout=subprocess.PIPE)
   p3.communicate()

   return 'p1_value'
   #|create_article.py|parse_article_html.py

   #   subprocess.call(create, shell=True) # saved in tmp_content.html html   

#   create = 'touch {}/{}'.format(script_path,'foooooooooooo') ## ChHANGE TO CHICHI   



value = update()
print "Content-type: text/html;charset=utf-8"
print
print """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
</head>
<body>
<p>Update taking place</p>
<p>{}</p>
</body></html>""".format(value)

       

      



