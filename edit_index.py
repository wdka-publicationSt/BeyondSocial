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
import html5lib, urllib2, json

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



def api_categoriesFromPage(page):
    '''Find all the categories, and their parent category of a page '''
    topic = []
    query = 'action=query&titles={}&prop=categories'.format(page)
    url = endpoint + query
    request = urllib2.urlopen(url)
#    print
#    print 'categories',url
#    print
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


def api_PublishMe_pages():
    '''Finds all pages within 04_Publish_Me category and returns a dictionary with info on those pages'''
    dict_articles = {}
    query = endpoint + 'action=query&list=categorymembers&cmtitle=Category:04_Publish_Me'
#    print 'Category: ', query
    url = endpoint + query
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
#    print '04_Publish_Me PAGES', jsonp['query']['categorymembers']

    for page in  jsonp['query']['categorymembers']:      
        page['title'] = (page['title']).replace(" ", "_") #use snakecase for page titles
#        print 'page', page
        article_meta = api_page(page['title'], 'meta')
#        print 'article_meta', article_meta
        categoriesFromPage = api_categoriesFromPage(page['title'])
        category_topic = categoriesFromPage[0]
        category_section = categoriesFromPage[1]
        category_issue = categoriesFromPage[2]

        dict_articles[ str(page['title']) ] = { 'pageid': article_meta['pageid'], 
                                            'touched': str(article_meta['touched'])[:-1],
                                            'topic': category_topic,
                                            'section': category_section,
                                            'issue': category_issue,
                                            } 
    return dict_articles


def insert_element(parent_el, insert_el, articles_dict, article):
    # print 'INSERT ELEMENTS'
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
    grandchild_a.set('href', 'articles/'+((article.split('/'))[-1])+'.html' )
    print article, articles_dict[article]['section']

    # print ET.tostring(child_li)

def update_element(tree, update_el_xpath, update_el, update):
    to_beupdated_el = tree.find(update_el_xpath)
    to_beupdated_el.set(update_el, update)
    return to_beupdated_el.get('data-section')#template_article.html)


def edit_index(articles_dict, index_path ): 
    ''' Compares articles_dicti with the index.html file 
    if there are new articles or updates in wiki:
    def adds them to index file, and triggers the creation of the content file for that article (via wiki_2_html def)'''
    index_file = open(index_path, 'r') 
    index_tree = html5lib.parse(index_file, namespaceHTMLElements=False)
    index_items = index_tree.findall('.//ul/li')
    li_data_name = [ (li.get('data-name')).encode('utf-8') for li in index_items]
    li_data_touched = [ (li.get('data-touched')).encode('utf-8') for li in index_items]

    for article in articles_dict.keys():  # compare the api results to the contents of index.html
        if article in li_data_name:
            article_pos = li_data_name.index(article)
#            print "ARTICLE IN INDEX", article, article_pos
            if li_data_touched[article_pos] != articles_dict[article]['touched']:
#                print "NOT SAME TOUCHED TIME", "update index"
                touched_time=articles_dict[article]['touched']
                section = update_element(index_tree, './/ul/li[@data-name="{}"]'.format(article), 'data-touched', touched_time)
                print article, section

        else:
#            print "ARTICLE MISSING FROM INDEX", article
            issue = 'list_' + (((articles_dict[article])['issue']).replace(" ","_")).lower()
            index_ul = index_tree.find('.//ul[@id="'+issue+'"]')
            insert_element(index_ul, 'li', articles_dict, article) #insert li into ul


    # if article is in index but Not in articles_dict: remove it
    for li in index_items:
        dataname =li.get('data-name')
        if dataname not in articles_dict.keys():
#            print 'article not in articles_dict', dataname
            uls = (index_tree.findall('.//ul[@class="list"]'))
            for ul in uls:                
                ul_lis = ul.findall('.//li[@data-name="{}"]'.format(dataname))
                if ul_lis:
                    ul.remove(ul_lis[0])

#    print ET.tostring(index_tree)
    write_html_file(ET.tostring(index_tree), 'index.html')

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




articles_issue_dic = api_PublishMe_pages()
edit_index(articles_issue_dic, 'index.html')
