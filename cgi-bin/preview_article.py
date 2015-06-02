#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, urllib, urllib2, json, subprocess

file_template='/var/www/beyond-social.org/html/template_article.html'
file_tmp='/var/www/beyond-social.org/html/articles/tmp_content.mw'

sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://beyond-social.org/wiki/api.php?format=json&"
issue_names = ["Test", "Redesigning Business"] 

def api_page(pagename, info):
    if info == 'content':        
        url = endpoint + 'action=query&titles={}&prop=revisions&rvprop=content'.format(pagename)
    elif info == 'meta':
        url = endpoint + 'action=query&titles={}&prop=info'.format(pagename)
#        print 'META URL', url

    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read() )
#    print jsonp
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


def pandoc(savepath, mw_content, pagename, in_section, in_topic, in_issue, in_issuename ):
    '''uses pandoc to convert mediawiki syntax to html'''        
    mw = open(file_tmp, 'w') 
    mw.write(mw_content.encode('utf-8'))
    mw.close()
    savepath = urllib.unquote(savepath)
    pagename = urllib.unquote(pagename)
    pandoc = 'pandoc -s -f mediawiki -t html5 \
--template {template} \
--variable title="{title}" \
--variable section="{section}" \
--variable topics="{topics}" \
--variable issueName="{iname}" \
--variable issueNumber="{inum}" \
{tmp} -o "{output}"'.format( template=file_template, title=(pagename).replace("_"," "), section=in_section, topics=in_topic, iname=in_issuename, inum=in_issue, tmp=file_tmp, output=savepath)    
    subprocess.call(pandoc, shell=True) # saved in tmp_content.html html
    html = open(file_tmp, 'r') #rea the saved html article content
    html = html.read()
    return html

def touch(savepath):
    cmd = 'touch {}'.format(savepath)
    subprocess.call(cmd, shell=True)
    
def wiki_2_html(mw_pagename, section , topic, issue): 
    '''convert wiki pages to html files'''
    savepath = '/var/www/beyond-social.org/html/preview/{}.html'.format(mw_pagename)
    content_mw = api_page_content(mw_pagename)
    if content_mw:
        issuenumber = int(issue[-1])
        issuename = issue_names[issuenumber]
        content_html = pandoc(savepath, content_mw, mw_pagename, section , topic, issue, issuename)
        print content_html

#     touch(savepath)


mw_pagename = sys.argv[1]
wiki_2_html(mw_pagename, 'preview' , 'preview', '0') 











