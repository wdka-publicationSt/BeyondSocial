#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import xml.etree.ElementTree as ET
import html5lib
import urllib, urllib2, json, subprocess
import sys, os, pprint

#import edit_html #  
#from edit_html import edit_html_media

sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://beyond-social.org/wiki/api.php?format=json&"
issue_names = ["Test", "Beyond Social"] 

def api_page(pagename, info):
    if info == 'content':        
        url = endpoint + 'action=query&titles={}&prop=revisions&rvprop=content'.format(pagename)
    elif info == 'meta':
        url = endpoint + 'action=query&titles={}&prop=info'.format(pagename)
#        print 'META URL', url

    print url
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read() )
    print jsonp
    json_dic= (jsonp.get('query').get('pages'))
    page_id =  json_dic.keys()[0]
    page_content = json_dic.get(page_id)
    return page_content


def api_page_content(pagename):
    page = api_page(pagename, 'content')
#    print 'PAGE', pagename
    content = ((page.get('revisions'))[0])['*']
    return content
#    print json.dumps( revisions, sort_keys=True, indent=4) ## see response



def pandoc(mw_content, pagename, in_section, in_topic, in_issue, in_issuename ):
    '''uses pandoc to convert mediawiki syntax to html'''
    mw = open('articles/tmp_content.mw', 'w') 
    mw.write(mw_content.encode('utf-8'))
    mw.close()
    pandoc = 'pandoc -s -f mediawiki -t html5 --template template_article.html --variable title="{title}" --variable section="{section}" --variable topics="{topics}" --variable issueName="{iname}" --variable issueNumber="{inum}" articles/tmp_content.mw -o articles/{htmlfile}.html'.format(title=pagename, section=in_section, topics=in_topic, iname=in_issuename, inum=in_issue, htmlfile=pagename)
    print 'pandoc'
    subprocess.call(pandoc, shell=True) # saved in tmp_content.html html
    html = open('tmp_content.html', 'r') #write mediawiki content to html in tmp_content.html
    html = html.read()
    return html

def wiki_2_html(mw_page, section , topic, issue): 
    '''convert wiki pages to html files'''
    html_file = ((mw_page.split('/'))[-1]) + '.html'
    content_mw = api_page_content(mw_page) 
    if content_mw:    
        issuenumber = int(issue[-1])
        issuename = issue_names[issuenumber]
        content_html = pandoc(content_mw, mw_page,  section , topic, issue, issuename)
#        print content_html
#        full_html = template(mw_page, content_html, article_template) 
#       edit_html_media(full_html , endpoint, html_file)
#     #    print full_html


for line in sys.stdin.readlines():
    stdin_input = (line.replace("\n","")).split(" ; ")
    print stdin_input
    article = stdin_input[0]
    issue = stdin_input[1]
    section = stdin_input[2]
    topic = stdin_input[3]
    

    print article, section
    wiki_2_html(article, section , topic, issue) # ADD Article






