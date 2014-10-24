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
 

def prepare_response(api, info): 
    '''prepares responses from api'''
    request = urllib2.urlopen(api)
    jsonp = json.loads(request.read() )
    json_dict= (jsonp.get('query').get('pages'))
    page_id =  json_dict.keys()[0]
    json_dict = json_dict.get(page_id)
    if info in ['categories'] : #if info=categories Output: category_list. 
        #categories: ['BeyondSocial', 'Issue0', 'Test']
        category_list = json_dict.get('categories')
        category_list = [  ((category['title'].encode('utf-8')).replace('Category:', '')).replace(' ','_') for category in category_list]
        response = category_list
    else:  #if info=content|meta Output: json_dict
        response = json_dict 
    return response


def api_page(pagename, info):
    '''ALL THE INFO ON AN ARTICLE: content, meta, categories, ''' 

    if info == 'content':        
        url = endpoint + 'action=query&titles={}&prop=revisions&rvprop=content'.format(pagename) 
        print 'CONTENT', url
    elif info == 'meta':
        url = endpoint + 'action=query&titles={}&prop=info&inprop=protection'.format(pagename)
        print 'META', url

    elif info == 'categories':
        url = endpoint + 'action=query&titles={}&prop=categories'.format(pagename)
        print 'CATEGORIES', url

    response = prepare_response(url, info)
    return response


def api_page_content(pagename): # MOVE THIS def INSIDE prepare_response ??
    page = api_page(pagename, 'content')
    print 'PAGE', pagename
    content = ((page.get('revisions'))[0])['*']
    return content
#    print json.dumps( revisions, sort_keys=True, indent=4) ## see response
    

def api_page_protection(pagename):  #IS THIS NEEDED? CAN'T ONLY api_page_content BE USED?
    # MOVE THIS def INSIDE prepare_response ??
    page = api_page(pagename, 'meta')
#    print 'Keys', page.keys()
    page_protection = page.get('protection')
    if page_protection: # page is protected
        print "PROTECTED PAGE"
        return api_page_content(pagename)
    else:       
        print 'PAGE NOT PROTECTED :('

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




################### index #######################

def api_pagesInIssue(issue): 
    '''Finds all pages within IssueN category
    Returns a DICTIONARY with metadata(page id, touched date) and category list of those pages,
    if they protected.    
    '''    
    dict_pagesInIssue = {}
    query = endpoint + 'action=query&list=categorymembers&cmtitle=Category:{}'.format(issue)
    print 'Category: ', query
    url = endpoint + query
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    print 'JSONP', jsonp['query']['categorymembers']

    for item in  jsonp['query']['categorymembers']:      
        article_meta = api_page(item['title'], 'meta')
        article_categories = api_page(item['title'], 'categories')

        if len(article_meta['protection']) > 0:
            dict_pagesInIssue[ str(item['title']) ] = { 'pageid': article_meta['pageid'], 
                                           'touched': str(article_meta['touched'])[:-1],
                                                        'categories': article_categories,
                                           } 
    return dict_pagesInIssue


def index_article_add(ul):
    '''adds <li> containing new articles to index <ul>'''
    child_li = ET.SubElement(ul, 'li') # added news
    grandchild_a = ET.SubElement(child_li, 'a') # added new
    return child_li, grandchild_a

def index_article_set(article_name, child_li, grandchild_a, dictionary):
    '''sets index's <li> with atrributes and values'''
    child_li.set('data-name', article_name )
    child_li.set('data-touched', dictionary[article_name]['touched'])            
    grandchild_a.text = article_name
    grandchild_a.set('href', 'html_articles/'+((article_name.split('/'))[-1])+'.html' )
    grandchild_a.set('data-name', article_name )
    categories = ' '.join(dictionary[article_name]['categories'])
    child_li.set('data-categories', categories )
    wiki_2_html(article_name) # CREATE article's to content file with def wiki_2_html


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
        if article not in index_items_data_name: #if new
#            print 'NEW ARTICLE', article
            li_anchor = index_article_add(index_ul) # add
            index_article_set(article, li_anchor[0], li_anchor[1], articles_dict) # set
            wiki_2_html(article) # CREATE article's to content file with def wiki_2_html
        else: # if already in index
            article_pos = index_items_data_name.index(article)
            if index_items_data_touched[article_pos] != articles_dict[article]['touched']: # check need for update 
#                print "NOT SAME TOUCHED TIME - UPDATING", article
                li_found = index_tree.find('.//li[@data-name="{}"]'.format(article))
                a_found =  index_tree.find('.//a[@data-name="{}"]'.format(article))
                index_article_set(article, li_found, a_found, articles_dict) # set
                wiki_2_html(article) # CREATE article's to content file with def wiki_2_html

    for article in index_items_data_name: # if category was removed
        if article not in articles_dict.keys():  
            li_found = index_tree.find('.//li[@data-name="{}"]'.format(article))
#            print "MISSING ARTICLE FROM DIC", article, ET.tostring(li_found)
            index_ul.remove(li_found)

#    print ET.tostring(index_tree)
    write_html_file(ET.tostring(index_tree), 'issue0_index.html')



## Create index
#index_ul = api_pagesInIssue('Issue0')
#index = template('index', index_ul, index_template)
#print index
#write_html_file(index, 'issue0_index.html')


articles_issue_dic = api_pagesInIssue('Issue0')
pprint.pprint(articles_issue_dic, width=1)
edit_index(articles_issue_dic, 'issue0_index.html')


#wiki_2_html(sys.argv[1]) 
