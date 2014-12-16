#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############
# Edit the index sorting articles according to topic, section and issue
#####

#
import xml.etree.ElementTree as ET
import html5lib, urllib2, json, pprint, subprocess

sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://beyond-social.org/wiki/api.php?format=json&"

category_topic = ['Aesthetics', 'Bottom-up', 'Economics', 'Failures', 'Participation', 'Politics', 'Strategies', 'Transformation', 'Visions', 'Technology']
category_section = ['Discourse', 'Introduction', 'Projects', 'Proposals' ]
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
#    issue="Issue 2"
#    print
#    print 'categories',url
#    print
    jsonp = json.loads(request.read())    
    json_dic = jsonp['query']['pages']
    page_id =  json_dic.keys()[0]
    page_categories = json_dic[page_id][u'categories']
    for entry in page_categories:
        category =  (entry[u'title'].encode('utf-8')).replace('Category:', '')
        if 'Issue' in category:  
            issue = category          
        elif category in category_topic:
            topic.append(category)
        elif category in category_section:
            section = category
    # print 'issue:', issue
    # print (topic, section, issue)        
    # print
    return (topic, section, issue)


def api_PublishMe_pages():
    '''Finds all pages within 04_Publish_Me category and returns a dictionary with info on those pages'''
    dict_articles = {}
    query = endpoint + 'action=query&list=categorymembers&cmlimit=500&cmtitle=Category:04_Publish_Me'
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
                                            'all': [],
                                            } 
    return dict_articles


def insert_element(parent_el, insert_el, articles_dict, article):
    # print 'INSERT ELEMENTS'
    child_li = ET.SubElement(parent_el, insert_el)
    child_li.set('data-name', article )
    child_li.set('data-touched', articles_dict[article]['touched'])
    child_li.set('data-section', articles_dict[article]['section'] )
    child_li.set('data-issue', articles_dict[article]['issue'] )
    keys = articles_dict[article].keys()
#    all_categories = [item for item in keys if item in  ]
    all_categories = articles_dict[article]['all']
    categories = ['issue', 'section', 'topic'] 
    for item in categories:
        if type(articles_dict[article][item]) is str:
            all_categories.append(articles_dict[article][item])
        elif type(articles_dict[article][item]) is list:
            for entry in articles_dict[article][item]:
                all_categories.append(entry)
    all_categories = " ".join(all_categories)
    child_li.set('class', all_categories )
    child_li.set('data-categories', all_categories )
    grandchild_a = ET.SubElement(child_li, 'a')
    grandchild_a.text = (article).replace("_"," ")
    grandchild_a.set('href', 'articles/'+((article.split('/'))[-1])+'.html' )
    # where is articles_dict being inserted all the categories into the topic key? 
    print article, ";", (articles_dict[article]['issue']).replace(" ","_"), ";", (articles_dict[article]['section']).replace(" ","_"), ";", " ".join(articles_dict[article]['topic'])

    # print ET.tostring(child_li)

def update_element(tree, update_el_xpath, update_el, update):
    to_beupdated_el = tree.find(update_el_xpath)
    to_beupdated_el.set(update_el, update)
    return to_beupdated_el.get('data-section')#template_article.html)


def edit_index(articles_dict, index_path ): 
    ''' Compares articles_dicti with the index.html file 
    if there are new articles or updates in wiki:
    def adds them to index file, and triggers the creation of the content file for that article (via wiki_2_html def)'''

    # dirty hack to have the sections ordered
    subprocess.call('cp index.html.bak index.html', shell=True) 
    #
    index_file = open(index_path, 'r') 
    index_tree = html5lib.parse(index_file, namespaceHTMLElements=False)
    uls = index_tree.findall('.//ul[@class="list"]')

    for article in articles_dict.keys():  
    #       print "ARTICLE MISSING FROM INDEX", article
        section =  articles_dict[article]['section']
        issue =  (articles_dict[article]['issue'].replace(" ","_")).lower()
        #print 'article', article, section, issue
        #print '---'
        current_ul = (index_tree.findall('.//ul[@id="section_{}"]'.format(section)))[0]
        #print ET.tostring(current_ul)
        #print '------------'
        insert_element(current_ul, 'li', articles_dict, article) #insert li into ul
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
