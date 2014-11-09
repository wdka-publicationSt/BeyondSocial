#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############
# TO DO
# bulding index
# 
#
# place index.html.bak in git


# wiki_2_html(article)  # TO BE DEALT WITH 
#
# Bugs 
# iframe creation in youtube tag
#####

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
endpoint = "http://beyond-social.org/wiki/api.php?format=json&"

category_topic = ['Aesthetics', 'Bottom-up', 'Economics', 'Failures', 'Participation', 'Politics', 'Strategies', 'Transformation', 'Visions']
category_section = ['Discourses', 'Introduction', 'Projects', 'Proposals' ]
category_state = [ '01 Write Me', '02 Edit Me', '03 Proof Me', '04 Publish Me']



def write_html_file(html_content, filename):
    doctype = "<!DOCTYPE HTML>"
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
        url = endpoint + 'action=query&titles={}&prop=revisions&rvprop=content'.format(pagename)
#        print 'CONTENT URL', url
    elif info == 'meta':
        url = endpoint + 'action=query&titles={}&prop=info'.format(pagename)
#        print 'META URL', url
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read() )
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


def wiki_2_html(mw_page): 
    '''convert wiki pages to html files'''
    html_file = ((mw_page.split('/'))[-1]) + '.html'
    content_mw = api_page_content(mw_page) 
    if content_mw:    
        content_html = pandoc(content_mw)
        full_html = template(mw_page, content_html, article_template) 
        edit_html_media(full_html , endpoint, html_file)

    #    print full_html

#wiki_2_html(sys.argv[1]) 





################### index #######################


def api_categoriesFromPage(page):
    '''Find all the categories, and their parent category of a page '''
    topic = []
    query = 'action=query&titles={}&prop=categories'.format(page)
    url = endpoint + query
    request = urllib2.urlopen(url)
    print
    print 'categories',url
    print
    jsonp = json.loads(request.read())    
    json_dic = jsonp['query']['pages']
    page_id =  json_dic.keys()[0]
    page_categories = json_dic[page_id][u'categories']
    for entry in page_categories:
        category =  (entry[u'title'].encode('utf-8')).replace('Category:', '')
        if category in category_topic:
            topic.append(category)
        elif category in category_section:
            section = category
        elif 'Issue'in category:
            issue = category
    return (topic, section, issue)



#def api_pagesInCategory(category): 

def api_PublishMe_pages():
    '''Finds all pages within 04_Publish_Me category and return a dictionary with info on those pages'''
    dic_categ = {}
    query = endpoint + 'action=query&list=categorymembers&cmtitle=Category:04_Publish_Me'
    print 'Category: ', query
    url = endpoint + query
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    print '04_Publish_Me PAGES', jsonp['query']['categorymembers']

    for page in  jsonp['query']['categorymembers']:      
        page['title'] = (page['title']).replace(" ", "_") #use snakecase for page titles
        print 'page', page
        article_meta = api_page(page['title'], 'meta')
        print 'article_meta', article_meta
        categoriesFromPage = api_categoriesFromPage(page['title'])
        category_topic = categoriesFromPage[0]
        category_section = categoriesFromPage[1]
        category_issue = categoriesFromPage[2]

        dic_categ[ str(page['title']) ] = { 'pageid': article_meta['pageid'], 
                                            'touched': str(article_meta['touched'])[:-1],
                                            'topic': category_topic,
                                            'section': category_section,
                                            'issue': category_issue,
                                            } 
    return dic_categ 



def insert_element(parent_el, insert_el, articles_dict, article):
    print 'INSERT ELEMENTS'
    child_li = ET.SubElement(parent_el, insert_el)
    child_li.set('data-name', article )
    child_li.set('data-touched', articles_dict[article]['touched'])
    child_li.set('data-section', articles_dict[article]['section'] )
    child_li.set('data-issue', articles_dict[article]['issue'] )
    all_categories = articles_dict[article]['topic']
    all_categories.append( articles_dict[article]['issue'])
    all_categories.append(articles_dict[article]['section'])
    all_categories = " ".join(all_categories)
    child_li.set('class', all_categories )
    child_li.set('data-categories', all_categories )
    grandchild_a = ET.SubElement(child_li, 'a')
    grandchild_a.text = article
    grandchild_a.set('href', 'html_articles/'+((article.split('/'))[-1])+'.html' )
#    print ET.tostring(child_li)

def update_element(tree, update_el_xpath, update_el, update):
    to_beupdated_el = tree.find(update_el_xpath)
    to_beupdated_el.set(update_el, update)

def edit_index(articles_dict, index_path ): 
    ''' Compares articles_dictionary with the index file 
    if there are new articles in mediawiki:
    def adds them to index file, and triggers the creation of the content file for that article (via wiki_2_html def)'''
    index_file = open(index_path, 'r') 
    index_tree = html5lib.parse(index_file, namespaceHTMLElements=False)
    index_items = index_tree.findall('.//ul/li')
    li_data_name = [ (li.get('data-name')).encode('utf-8') for li in index_items]
    li_data_touched = [ (li.get('data-touched')).encode('utf-8') for li in index_items]

    print 'data_name', li_data_name
    print 'data_touched', li_data_touched
    
    for article in articles_dict.keys():  # compare the api results to the contents of index.html
        if article in li_data_name:
            article_pos = li_data_name.index(article)
            print "ARTICLE IN INDEX", article, article_pos
            # find touched time
            if li_data_touched[article_pos] != articles_dict[article]['touched']:
                print "NOT SAME TOUCHED TIME"
                # update index 
                touched_time=articles_dict[article]['touched']
                print 'touched_time', touched_time
                update_element(index_tree, './/ul/li[@data-name="{}"]'.format(article), 'data-touched', touched_time)


                # # find li_data_name item corresponding to article_post
                # this_li = index_tree.find('.//ul/li[@data-name="{}"]'.format(article))
                # print 'THIS LI', this_li              
                # # change data-touched to current
                # this_li.set('data-touched', touched_time)



##                wiki_2_html(article) # UPDATE Article
            else:
                print "SAME TOUCHED TIME" # do nothing
        else:
            print "ARTICLE MISSING FROM INDEX", article
            # add article item to index
            # FIND UL WHERE THIS ARTICLE BELONGS TO
            issue = 'list_' + (((articles_dict[article])['issue']).replace(" ","_")).lower()
            index_ul = index_tree.find('.//ul[@id="'+issue+'"]')
            insert_element(index_ul, 'li', articles_dict, article) #insert li into ul
            ##wiki_2_html(article) # ADD Article

#    print ET.tostring(index_tree)
    write_html_file(ET.tostring(index_tree), 'index.html')


    # for li in index_items:  compare the api results to the contents of index.html
    #     print "-----------"
    #     print "ITEM", li.get('data-name').text 
    #     print "-----------"
    #     print 'li_data_name', li_data_name

    #     if li.get('data-name') not in li_data_name:
    #         print "missing article item", articles_dict[article]



            # check date 

    #        print "ARTICLE PRESENT:", article, "in position:", article_pos



'''

    for article in articles_dict.keys():  # compare the api results to the contents of index.html
        print "***********"
        print "ARTICLE", article
        print "***********"

        if article not in index_items_data_name:   # is article in index_items?
            print "ARTICLE MISSING", article
            # ADD Article  to index
            #insert elements
            child_li = ET.SubElement(index_ul, 'li')
            child_li.set('data-name', article )
            child_li.set('data-touched', articles_dict[article]['touched'])
            child_li.set('data-section', articles_dict[article]['section'] )
            child_li.set('data-issue', articles_dict[article]['issue'] )
            all_categories = articles_dict[article]['topic']
            all_categories.append( articles_dict[article]['issue'])
            all_categories.append(articles_dict[article]['section'])
            all_categories = " ".join(all_categories)
            child_li.set('class', all_categories )
            child_li.set('data-categories', all_categories )
            grandchild_a = ET.SubElement(child_li, 'a')
            grandchild_a.text = article
            grandchild_a.set('href', 'html_articles/'+((article.split('/'))[-1])+'.html' )

            #wiki_2_html(article) # CREATE ARTICLE'S TO CONTENT


        else: 
            article_pos = index_items_data_name.index(article)
            print "ARTICLE PRESENT:", article, "in position:", article_pos

            # touched time
            if index_items_data_touched[article_pos] != articles_dict[article]['touched']:
                print "NOT SAME TOUCHED TIME"
#                wiki_2_html(article) # UPDATE

                # if yes:    
                # if is touched date in index.html older that the one from API?
                # yes:
                # UPDATE content file & index.html
                
                # if not: 
                # ADD to content file & index.hmlt 

        print article, articles_dict[article]
        print 
        print ET.tostring(index_tree)
        write_html_file(ET.tostring(index_tree), 'index.html')
'''
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
#write_html_file(index, 'issue0_index.htmlye')

#parse_index('issue0_index.html')

#issue = 'Issue_0'

articles_issue_dic = api_PublishMe_pages()
pprint.pprint(articles_issue_dic, width=1)

edit_index(articles_issue_dic, 'index.html')
