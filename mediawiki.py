#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############
# TO DO
# * finish  def edit_index - so that index is created and new articles addedd
#
# Bugs 
# iframe creation in youtube tag
'''
<Element 'iframe' at 0x7f7db6fd6710> <iframe width="560" height="315" frameborder="0" allowfullscreen="allowfullscreen" src="http://www.youtube.com/embed/hIR3VW5DQ_o" /> <Element u'p' at 0x7f7db701a240>
Traceback (most recent call last):
  File "./mediawiki.py", line 264, in <module>
    edit_index(articles_issue_dic, 'issue0_index.html')
  File "./mediawiki.py", line 203, in edit_index
    wiki_2_html(article) 
  File "./mediawiki.py", line 130, in wiki_2_html
    edit_html_media(full_html , endpoint, html_file)
  File "/home/andre/Documents/WdKA/BeyondSocial/wiki_api/edit_html.py", line 45, in edit_html_media
    p.append(embed_element)
TypeError: must be Element, not Element

'''
###


#
import xml.etree.ElementTree as ET
import html5lib
import urllib, urllib2, json, subprocess
import sys, os, pprint
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
    elif info == 'meta':
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
    page = api_page(pagename, 'meta')
#    print 'Keys', page.keys()
    page_protection = page.get('protection')
    if page_protection: # page is protected
        print "PROTECTED PAGE"
        return api_page_content(pagename)
    else:       
        print 'PAGE NOT PROTECTED :('
    print
#        api_page_content(pagename, page_title)


def wiki_2_html(mw_page): 
    '''convert wiki pages to html files'''
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





################### index #######################

def api_pagesInCategory(category): 
    '''**finds all pages within category and return a dictionary with info on those pages**'''
    dic_categ = {}
    query = endpoint + 'action=query&list=categorymembers&cmtitle=Category:{}'.format(category)
    print 'Category: ', query
    url = endpoint + query
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    print 'JSONP', jsonp['query']['categorymembers']

    for item in  jsonp['query']['categorymembers']:      
        article_meta = api_page(item['title'], 'meta')
        dic_categ[ str(item['title']) ] = { 'pageid': article_meta['pageid'], 
                                       'touched': str(article_meta['touched'])[:-1],
                                       } 
    return dic_categ




def edit_index( articles_dict, index_path ): 
    ''' Compares articles_dictionary with the index file 
    if there are new articles in mediawiki:
    def adds them to index file, and triggers the creation of the content file for that article (via wiki_2_html def)'''

    index_file = open(index_path, 'r') 
    index_tree = html5lib.parse(index_file, namespaceHTMLElements=False)
    index_ul = index_tree.findall('.//ul')[0]
    index_items = index_tree.findall('.//li')
    index_items_data_name = [ (li.get('data-name')).encode('utf-8') for li in index_items]
    index_items_data_touched = [ (li.get('data-touched')).encode('utf-8') for li in index_items]

    for article in articles_dict.keys():  # compare the api results to the contents of index.html
        # is article in index_items?
        if article not in index_items_data_name:
            print "ARTICLE MISSING", article
            # ADD Article  to index
            #insert elements
            child_li = ET.SubElement(index_ul, 'li')
            child_li.set('data-name', article )
            child_li.set('data-touched', articles_dict[article]['touched'])
            grandchild_a = ET.SubElement(child_li, 'a')
            grandchild_a.text = article
            grandchild_a.set('href', 'html_articles/'+((article.split('/'))[-1])+'.html' )
            
            wiki_2_html(article) # CREATE article's to content file with def wiki_2_html
        else: 
            article_pos = index_items_data_name.index(article)
            print "ARTICLE PRESENT:", article, "in position:", article_pos

            # touched time
            if index_items_data_touched[article_pos] != articles_dict[article]['touched']:
                print "NOT SAME TOUCHED TIME"
            wiki_2_html(article) # UPDATE

                # if yes:    
                # if is touched date in index.html older that the one from API?
                # yes:
                # UPDATE content file & index.html
                
                # if not: 
                # ADD to content file & index.hmlt 

        print article, articles_dict[article]
        print 
        print ET.tostring(index_tree)
        write_html_file(ET.tostring(index_tree), 'issue0_index.html')

#         for key in articles_dict[article].keys():
#             print key, articles_dict[article][key]



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

#parse_index('issue0_index.html')

articles_issue_dic = api_pagesInCategory('Issue0')
pprint.pprint(articles_issue_dic, width=1)
edit_index(articles_issue_dic, 'issue0_index.html')
