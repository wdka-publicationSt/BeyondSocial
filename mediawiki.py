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
#endpoint = "http://en.wikipedia.org/w/api.php?format=json&"

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
    html = open('page_wiki.html', 'w') #write mediawiki content to content.mw
    html.write(html_page.encode('utf-8'))
    return html_page

def pandoc(mw_content):
    '''uses pandoc to convert mediawiki syntax to html'''

    mw = open('content.mw', 'w') 
    mw.write(mw_content.encode('utf-8'))
    mw.close()
    pandoc = 'pandoc -f mediawiki -t html5  content.mw -o content.html'
    subprocess.call(pandoc, shell=True) # saved in content.html html
    html = open('content.html', 'r') #write mediawiki content to content.mw
    html = html.read()
    return html
 


def api_page(pagename, info):
    if info == 'content':        
        url = endpoint + 'action=query&titles={}&prop=revisions&rvprop=content'.format(pagename) #no protection info in this url
    elif info == 'protection':
        url = endpoint + 'action=query&titles={}&prop=info&inprop=protection'.format(pagename)

    print url
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read() )
    json_dic= (jsonp.get('query').get('pages'))
    page_id =  json_dic.keys()[0]
    page_content = json_dic.get(page_id)
    return page_content


def api_page_content(pagename):
    page = api_page(pagename, 'content')
    print 'PAGE', page
    # get title
    content = ((page.get('revisions'))[0])['*']
    return content
#    print json.dumps( revisions, sort_keys=True, indent=4) ## see response
    

def api_page_protection(pagename):
    page = api_page(pagename, 'protection')
    print 'Keys', page.keys()
    page_protection = page.get('protection')
    print 'page_protection', page_protection
    if page_protection: # page is protected
        print "PROTECTED PAGE"
        api_page_content(pagename)
    else:       
        print 'PAGE NOT PROTECTED :('


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



mw_page = sys.argv[1]
content_mw = api_page_protection(mw_page) #only retreive content if page is protected
# if not interested in Protection use
#content_mw=api_page_content(mw_page) 

if content_mw:    
    content_html = pandoc(content_mw)
    # TODO: parse content_html 
    # TO: replace relative file paths with  full url
    full_html = template(mw_page, content_html) 
    print full_html

