#! /usr/bin/env python
# -*- coding: utf-8 -*-

##############
# Edit the index sorting articles according to topic, section and issue
#####

#
import xml.etree.ElementTree as ET
import html5lib, urllib2, json, pprint, subprocess
from urllib import quote as quote
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


def api_request(action, pagename):
    url = endpoint + action.format(pagename)
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read() )
    json_dic= (jsonp.get('query').get('pages'))
    page_id =  json_dic.keys()[0]
    page_content = json_dic.get(page_id)
    return page_content


def api_page_content(pagename):
    print 'starting api_page_content', pagename
    page = api_page(pagename, 'content')
    print 'PAGE', pagename
    content = ((page.get('revisions'))[0])['*']
    return content


def api_page(pagename, info):
    pagename = pagename.replace(" ", "_")
    if info == 'content':
        api_response = api_request('action=query&titles={}&prop=revisions&rvprop=content', pagename)
        page_content = ((api_response.get('revisions'))[0])['*']
        
    elif info == 'meta':
        page_content = api_request('action=query&titles={}&prop=info', pagename)

    elif info == 'articleimgs':
        page_content = api_request('action=query&titles={}&prop=images', pagename)

    elif info == 'imageinfo':
        page_content = api_request('action=query&titles={}&prop=imageinfo&iiprop=url&iiurlwidth=300', pagename)  # iiurlwidht dermines with of thumbnail 
        
    return page_content

def api_thumb_url(filename):
   '''get thumbnail url of image'''
   page_content_dict = api_page(filename, 'imageinfo')   
   if 'imageinfo' in page_content_dict.keys():
       thumburl = ((page_content_dict.get('imageinfo'))[0].get('thumburl'))
       return page_content_dict


def find_imgs(article):
    '''get all internal images from published articles:
    * query all images in  a article
    * for each image request a thumbnail
    * get the thumburl    
    '''
    page_content_dict = api_page(article, 'articleimgs')
    if 'images' in page_content_dict.keys():
        images_list = page_content_dict.get('images')
#        print 'images_list', images_list
        thumbs_list = []
        for img in images_list: # all images in article
            title = img.get('title')
            thumburl_json = api_thumb_url(title)
            if thumburl_json != None:
                thumburl = (thumburl_json.get('imageinfo')[0]).get('thumburl')
                thumbs_list.append(thumburl)
            else:
                thumburl = None
                
        return thumbs_list 
'''
thumburl {u'imagerepository': u'local', u'ns': 6, u'pageid': 244, u'imageinfo': [{u'url': u'http://beyond-social.org/wiki/images/c/ca/Rb-circular-dinsdag08.jpg', u'thumbheight': 200, u'thumburl': u'http://beyond-social.org/wiki/images/thumb/c/ca/Rb-circular-dinsdag08.jpg/300px-Rb-circular-dinsdag08.jpg', u'thumbwidth': 300, u'descriptionurl': u'http://beyond-social.org/wiki/index.php/File:Rb-circular-dinsdag08.jpg'}], u'title': u'File:Rb-circular-dinsdag08.jpg'}
'''                
                #RETURN SHOULD BE A HTML LIST (see Lasses' index page ) ALL THE IMAGE FROM THE ARTICLE




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


def api_author(pagetitle):
    content_mw = api_page(pagetitle, 'content') 
    if content_mw:
        content_list = content_mw.split('\n')
        if 'Author: ' in content_list[0]:
            author =  content_list[0].replace('Author:', '')
            content_list.remove(content_list[0])

        elif 'Authors: ' in content_list[0]:
            author =  content_list[0].replace('Authors:', '')
            content_list.remove(content_list[0])
        else:
            author = ''
            
        return author
'''
AUTHOR  Tabo Goudswaard, Deanna Herst & Iris Schutten
AUTHOR == " Iris Schutten" ==
AUTHOR 
AUTHOR == " Annelys de Vet" ==
AUTHOR == " Deanna Herst & Iris Schutten" ==
AUTHOR == " Pieter Haasnoot" ==
AUTHOR == " Lennart Pieters" ==
AUTHOR == " André Schaminee" ==
AUTHOR  Duzan Doepel
AUTHOR == " Joost Beunderman" ==
AUTHOR  Elise van Beurden, Niels Buwelda, Leon van Genderen, Richard Haag, Marleen Ooms, Leon Ragetlie, Zehra Sagay, David Verdonk & Deanna Herst
    
'''
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
        
        author = api_author( page['title'])
        
        dict_articles[ str(page['title']) ] = { 'pageid': article_meta['pageid'], 
                                                'touched': str(article_meta['touched'])[:-1],
                                                'topic': category_topic,
                                                'section': category_section,
                                                'issue': category_issue,
                                                'author': author,    
                                                'all': [],
                                            }
        
    return dict_articles




def insert_element(parent_el, insert_el, articles_dict, article, navigation, thumb, author):
    child_li = ET.SubElement(parent_el, insert_el)
    child_li.set('data-name', article )
    child_li.set('data-touched', articles_dict[article]['touched'])
    child_li.set('data-section', articles_dict[article]['section'] )
    child_li.set('data-issue', articles_dict[article]['issue'] )
    keys = articles_dict[article].keys()
    all_categories = articles_dict[article]['all']
    categories = ['issue', 'section', 'topic'] 

    for item in categories:
        if type(articles_dict[article][item]) is str and articles_dict[article][item] not in all_categories :
            all_categories.append(articles_dict[article][item])
        elif type(articles_dict[article][item]) is list:
            for entry in articles_dict[article][item]:
                if entry not in all_categories:
                    all_categories.append(entry)
                    
    all_categories = " ".join(all_categories)
    child_li.set('class', all_categories )
    child_li.set('data-categories', all_categories )
    grandchild_a = ET.SubElement(child_li, 'a')
    article = ((article.split('/'))[-1])
    url = quote(article+'.html') 
    grandchild_a.set('href', 'articles/'+url )

    if author is not None:
        grandchild_author = ET.SubElement(child_li, 'p')
        grandchild_author.text = author
        grandchild_author.set('class', 'authorTitle')
        
    if navigation is "text":        
        grandchild_a.text = (article).replace("_"," ")
        print "frontend", ";", article, ";", (articles_dict[article]['issue']).replace(" ","_"), ";", (articles_dict[article]['section']).replace(" ","_"), ";", " ".join(articles_dict[article]['topic'])
    elif navigation is "image":
        grandgrandchild_img = ET.SubElement(grandchild_a, 'img')
        grandgrandchild_img.set('src', thumb)

    # print ET.tostring(child_li)
    # print

    
def update_element(tree, update_el_xpath, update_el, update):
    to_beupdated_el = tree.find(update_el_xpath)
    to_beupdated_el.set(update_el, update)
    return to_beupdated_el.get('data-section')#template_article.html)



def check_index(articles_dict, index_path ):
    ''' Compares articles_dicti with the index.html file 
    if there are new articles or updates in wiki:
    def adds them to index file, and triggers the creation of the content file for that article (via wiki_2_html def)'''

    index_file = open(index_path, 'r') 
    index_tree = html5lib.parse(index_file, namespaceHTMLElements=False)
    index_items = index_tree.findall('.//ul/li')
    li_data_name = [ (li.get('data-name')).encode('utf-8') for li in index_items]
    li_data_touched = [ (li.get('data-touched')).encode('utf-8') for li in index_items]
    edit = 0

    for article in articles_dict.keys():  # compare the api results to the contents of index.html
        if article in li_data_name:
            article_pos = li_data_name.index(article)
            if li_data_touched[article_pos] != articles_dict[article]['touched']: # FOR TESTS REPLACE != for == than all articles wil be updated 
                edit =1
        else:
            edit = 1
        
    if edit == 1:
        edit_index(articles_issue_dic, 'index.html')        
    
def edit_index(articles_dict, index_path ): 
    '''edits the index.html'''
    subprocess.call('cp index.html.bak index.html', shell=True)     # dirty hack to have the sections ordered
    index_file = open(index_path, 'r') 
    index_tree = html5lib.parse(index_file, namespaceHTMLElements=False)
    uls = index_tree.findall('.//ul[@class="list"]')

    for article in articles_dict.keys():  
        #       print "ARTICLE MISSING FROM INDEX", article
        author =  articles_dict[article]['author']
        section =  articles_dict[article]['section']
        issue =  (articles_dict[article]['issue'].replace(" ","_")).lower()
        #print 'article', article, section, issue
        #print '---'
        current_ul = (index_tree.findall('.//ul[@id="section_{}"]'.format(section)))[0]
        #print ET.tostring(current_ul)
        #print '------------'
        insert_element(current_ul, 'li', articles_dict, article, 'text', None, author) #insert li into ul
        
        thumbs_list  = find_imgs(article) # THUMBNAILS # WORKING ON
        if thumbs_list:            
            current_ul = (index_tree.findall('.//ul[@class="{}"]'.format('imageNavigation')))[0]
            for thumb in thumbs_list:
                insert_element(current_ul, 'li', articles_dict, article, 'image', thumb, None) #insert li w/ images into ul.imageNavigation
        
    write_html_file(ET.tostring(index_tree), 'index.html')




            
    
def parse_index(filepath):
    input_file = open(filepath, 'r') 
    tree = html5lib.parse(input_file, namespaceHTMLElements=False)
    # find li
    for ul in tree.findall('.//ul'):        
#        print len(ul), 'ul', ET.tostring(ul), type(ul), ul
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
#    print ET.tostring(tree)




articles_issue_dic = api_PublishMe_pages()
check_index(articles_issue_dic, 'index.html')

