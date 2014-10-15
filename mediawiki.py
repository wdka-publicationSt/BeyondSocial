#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import html5lib
import urllib, urllib2, json, subprocess
import sys, os
from django.template import Template, Context
from django.conf import settings
settings.configure() # We have to do this to use django templates standalone - see
# http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django
import edit_html #  
from edit_html import edit_html_media

sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://localhost/wiki/api.php?format=json&"
#endpoint = "http://en.wikipedia.org/w/api.php?format=json&"

#query='action=query&list=categorymembers&cmtitle=Category:project'
#http://localhost/wiki/api.php?format=json&action=query&list=categorymembers&cmtitle=Category:project


def write_html_file(html_content, filename):
    doctype = "<!DOCTYPE html>"
    html = doctype + html_content #ET.tostring(tree,  encoding='utf-8', method='html')
    edited = open(filename, 'w') #write
    edited.write(html)
    edited.close()


def template(title, content, mytemplate):
    t = Template(mytemplate)
    c = Context({"title": title,
             "body":content})
    html_page = t.render(c)
    html = open('page_wiki.html', 'w') #write mediawiki content to content.mw
    html.write(html_page.encode('utf-8'))
    return html_page


################### index #######################

index_template = """
<html>
<head>
<title>{{ title }}</title>
<meta charset="utf-8" />
</head>
<body>
<h1>{{ title }}</h1>
<ul>
 {{ body | safe }}
</ul>
<hr/>
</body>
</html>
"""

def api_pagesInCategory( category): # find all pages within category
    query = endpoint + 'action=query&list=categorymembers&cmtitle=Category:{}'.format(category)
    print 'Category: ', query
    url = endpoint + query
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    ul = ""
    for item in  jsonp['query']['categorymembers']:        
        wiki_url = 'http://localhost/wiki/index.php/' +  item['title']
        article_name = ( item['title'].split('/'))[-1]
        article_file =  (( item['title'].split('/'))[-1])+'.html'
        article_path = 'html_articles/'+ article_file
        html_li = '<li><a href="{url}">{name}</li>\n'.format(url=article_path, name=article_name)
        ul = ul+html_li
        print html_li#article_name, wiki_url, article_file
        print json.dumps(item, sort_keys=True, indent=4)    
    return ul

def parse_index(filepath):
    input_file = open(filepath, 'r') 
    tree = html5lib.parse(input_file, namespaceHTMLElements=False)

    # find li
    for ul in tree.findall('.//ul'):        
        print len(ul), 'ul', ET.tostring(ul), type(ul), ul
        for li in ul:
            print 'li', ET.tostring(li)

            # set attributes
            li_id = li.get('id')
            li.set('id', li_id+'_x')
            li.set('class', li_id+'_zz')
            print li_id
            
        #insert elements
        child = ET.SubElement(ul, 'li')
        child.text = 'new list item.'

    print ET.tostring(tree)


## Create index
#index_ul = api_pagesInCategory('Issue0')
#index = template('index', index_ul, index_template)
#print index
#write_html_file(index, 'issue0_index.html')

parse_index('issue0_index.html')



# instead of writing index from template parse exsiting index file


# use the index a the central point to:
# * create newpages
# * 


##################### content #########################

article_template = """
<html>
<head>
<title>{{ title }}</title>
<meta charset="utf-8" />
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
</body>
</html>
"""


def pandoc(mw_content):
    '''uses pandoc to convert mediawiki syntax to html'''
    mw = open('tmp_content.mw', 'w') 
    mw.write(mw_content.encode('utf-8'))
    mw.close()
    pandoc = 'pandoc -f mediawiki -t html5 tmp_content.mw -o tmp_content.html' 
    print 'pandoc'
    subprocess.call(pandoc, shell=True) # saved in tmp_content.html html
    html = open('tmp_content.html', 'r') #write mediawiki content to html in tmp_content.html
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
    print 'PAGE', pagename
    content = ((page.get('revisions'))[0])['*']
    return content
#    print json.dumps( revisions, sort_keys=True, indent=4) ## see response
    

def api_page_protection(pagename):
    page = api_page(pagename, 'protection')
#    print 'Keys', page.keys()
    page_protection = page.get('protection')
    if page_protection: # page is protected
        print "PROTECTED PAGE"
        return api_page_content(pagename)
    else:       
        print 'PAGE NOT PROTECTED :('
    print
#        api_page_content(pagename, page_title)


def wiki_2_html(mw_page): # convert wiki pages to html files
    html_file = ((mw_page.split('/'))[-1]) + '.html'
    content_mw = api_page_protection(mw_page) #retreive protected page mw content
    # if not interested in protected pages, use: 
       # content_mw = api_page_content(mw_page) 
    if content_mw:    
        content_html = pandoc(content_mw)
        full_html = template(mw_page, content_html, article_template) 
        edit_html_media(full_html , endpoint, html_file)
    #    print full_html

#wiki_2_html(sys.argv[1]) 
