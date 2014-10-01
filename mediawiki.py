#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2, json, subprocess
import sys
from django.template import Template, Context
from django.conf import settings
settings.configure() # We have to do this to use django templates standalone - see
# http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django


sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://localhost/wiki/api.php?format=json&"

#query='action=query&list=categorymembers&cmtitle=Category:project'
#http://localhost/wiki/api.php?format=json&action=query&list=categorymembers&cmtitle=Category:project

html_template = """
<html>
<head>
<title>{{ title }}</title>
<style type="text/css" media="screen">
  body{background:#cacc00;
  font-family: Sans;
    }
    
  a{color:#b213ab;}

  a:visited{color:#b213ab;}
</style>
</head>
<body>
<h1>{{ title }}</h1>
<hr/>
 {{ body | safe }}.
<hr/>
<p>end of page</p>
</body>
</html>
"""

def template(title, content):
    t = Template(html_template)
    c = Context({"title": title,
             "body":content})
    html_page = t.render(c)
    html = open('page.html', 'w') #write mediawiki content to content.mw
    html.write(html_page.encode('utf-8'))
    return html_page

def pandoc(mw_content):
    '''uses pandoc to convert mediawiki syntax to html'''

    mw = open('content.mw', 'w') #write mediawiki content to content.mw
    mw.write(mw_content)
    mw.close()
    pandoc = 'pandoc -f mediawiki -t html content.mw -o content.html'
    subprocess.call(pandoc, shell=True) # saved in content.html html
    html = open('content.html', 'r') #write mediawiki content to content.mw
    html = html.read()
    return html
 


def api_page(pagename):
    url = endpoint + 'action=query&titles={}&prop=revisions&rvprop=content'.format(pagename)
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read() )
    json_dic= (jsonp.get('query').get('pages'))
    page_id =  json_dic.keys()[0]
    page_content = json_dic.get(page_id)
    return page_content


def api_page_content(pagename):
    page = api_page(pagename)
    print 'PAGE', page
    # get title
    content = ((page.get('revisions'))[0])['*']
    return content
#    print json.dumps( revisions, sort_keys=True, indent=4) ## see response
    


def api_page_protection(pagename):
    page = api_page(pagename)              
    page_protection = page.get('protection')
    print 'protection',  page_protection
    print json.dumps( page, sort_keys=True, indent=4) ## see response        
# TODO check protection
#    if page_protection: # page is protected
#       content = ((page.get('revisions'))[0])['*']
        # print '--------------------------------------------'
        # print content
        # print '--------------------------------------------'
    # else:
    #     print 'nothing to show :('





def api_pagesInCategory( category):
    query = endpoint + 'action=query&list=categorymembers&cmtitle=Category:{}'.format(category)
    print query
    url = endpoint + query
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    for item in  jsonp['query']['categorymembers']:
        print item['title']
        print json.dumps(item, sort_keys=True, indent=4)

#api_pagesInCategory('project')
#api_page_protection('WDKA/BeyondSocial')

mw_page = sys.argv[1]
content_mw=api_page_content(mw_page) 
#print content_mw
content_html = pandoc(content_mw)
full_html = template(mw_page, content_html) 
print full_html

