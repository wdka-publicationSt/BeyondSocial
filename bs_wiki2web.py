#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import html5lib, urllib, pprint, collections, os
# unsued from bs_modules: replace_gallery, replace_video, index_addwork,
from argparse import ArgumentParser

##############
# REQUIRES:
# * pandoc 
# * python mwclient https://github.com/mwclient/mwclient 
# ** install$ sudo pip install mwclient
#############

#####
# BS topics, section, issue names:
####
category_topic = ['Aesthetics', 'Bottom-up', 'Economics', 'Failures', 'Participation', 'Politics', 'Strategies', 'Transformation', 'Visions', 'Technology']
category_section = ['Discourse', 'Introduction', 'Projects', 'Proposals', 'Methods' ]
issue_names = {'1': 'Redesigning Business', '2':'Education', '3':'Radical Reframing'}
issue_names = collections.OrderedDict(sorted(issue_names.items()))
issue_keys = issue_names.keys()
issue_templates = {}
dir_templates = os.path.abspath('templates') #templates dir
for f in os.listdir(dir_templates): #generate issue_templates
    n = f[0]
    if n not in issue_templates.keys():
        issue_templates[n] = {}
    issue_templates[n][(f.split('-'))[1]] = f

#pprint.pprint(issue_templates)


#####
# Args
####
p = ArgumentParser()
p.add_argument('-V', '--version', action='version', version='version 1.0')
p.add_argument("--local", action='store_true', help="use local when running the script on local machine")
p.add_argument("--host", default="beyond-social.org")
p.add_argument("--path", default="/wiki/", help="path: should end with /")
p.add_argument("--category", "-c", nargs="*", default=[['04 Publish Me']], action="append", help="Category to query. Use: -c foo -c bar to intersect multiple categories")
p.add_argument("--preview", help='Preview a specific page. Will override category querying. Use: --page "Name Of Wiki Page"')
#p.add_argument("--preview", action='store_true', help='Preview mode flag. Requires --page "Name Of Wiki Page" ') 
args = p.parse_args()
local = args.local
if local is True:
    wd = '.'
else:
    wd = '/var/www/beyond-social.org/html' #working directiory

from bs_modules import pandoc2html, write_html_file, mw_cats, mw_page_imgsurl, mw_img_url, mw_page_text, mwsite, mw_page_cats, mw_page, remove_cats, find_authors, replace_video, replace_img_a_tag
    
######
# DEFS:  create_page create_index
######
def create_page(memberpages, mode):

    indexdict = {} #parent dict: contains articledict instances
    for member in memberpages:
        print 'MEMBER PAGE', member
        page = mw_page(site, member)
        page_name = page.name 
        page_cats = mw_page_cats(site, page) # [u'Category:Discourse', u'Category:Issue 1', u'Category:Economics', u'Category:Visions', u'Category:Transformation']
        #print 'PAGE_CATS >>> ', page_cats
        page_text = mw_page_text(site, page)
        page_imgs = mw_page_imgsurl(site, page)
        page_imgs = { key.capitalize():value for key, value in page_imgs.items()} # loop to capatalize keys, so can be called later
        articledict = {'Title': page_name, 'Content': page_text, 'Categories':page_cats, 'Images': page_imgs}

        if articledict['Content']: # if there is content --- clean and convert content to html
            articledict['Authors'], articledict['Content'] = find_authors(articledict['Content'])
            articledict['Content'] = remove_cats(articledict['Content'])
            articledict['Content'] = replace_video(articledict['Content'])
            articledict['Content'] = pandoc2html(articledict['Content']) # future: here we will call mw render
            articledict['Category Topics'] = [] # as to be appended in loop below
            
            for entry in articledict['Categories']:
                category = (entry).replace('Category:', '')
                if 'Issue' in category:
                    articledict['Category Issue'] = category.replace('Issue ','')
                    #print 'articledict', articledict['Category Issue'], issue_names
                    # print type(articledict['Category Issue']), type( (issue_names[articledict['Category Issue']]).decode('utf-8'))
                    # print articledict['Category Issue']  + u' '+ (issue_names[articledict['Category Issue']]).decode('utf-8')
                    articledict['Category Issue'] = articledict['Category Issue']  + u' '+ (issue_names[articledict['Category Issue']]).decode('utf-8')
                    #pprint.pprint( articledict )
                    #.zfill()
                elif category in category_topic:
                    articledict['Category Topics'].append(category)
                elif category in category_section:
                    articledict['Category Section']= category
            articledict.pop('Categories') 

            # only if a page has a section + issue, it is further processed
            if 'Category Issue' in articledict.keys() and 'Category Section' in articledict.keys():
                issue = articledict['Category Issue'][0]
                article_template_file = issue_templates[issue]['article']
                print 
                print article_template_file
                print 
                article_template = open("{}/{}".format(dir_templates, article_template_file), "r") 

                #page_template = open("{}/article-template.html".format(wd), "r")
    
                
                # HTML tree  # create work page
                page_tree = html5lib.parse(article_template, namespaceHTMLElements=False)
                page_title = page_tree.find('.//title')
                page_title_h1 = page_tree.find('.//h1[@title="title"]')
                page_title.text = articledict['Title']
                page_title_h1.text = articledict['Title']
                print 'page_title:', articledict['Title']
                page_issue =  page_tree.find('.//span[@id="issue"]')


                page_issue.text = articledict['Category Issue']
                

                page_section = page_tree.find('.//span[@id="section"]')
                page_section.text = articledict['Category Section']
                page_topics =  page_tree.find('.//span[@id="topics"]')
                page_topics.text = " ".join(articledict['Category Topics'])
                page_author = page_tree.find('.//p[@class="authorTitle"]')
                page_author.text = articledict['Authors']

                page_content = page_tree.find('.//div[@class="content"]')
                content =  html5lib.parse(articledict['Content'], namespaceHTMLElements=False)
                bodycontent = content.findall('.//body/*') 
                for el in bodycontent:
                    page_content.append(el)
                # maybe above page_content can be ACCESSED + SIMPLY
                # but content comes wrapped in <html><body>

                # get imgs full url
                imgs = page_content.findall('.//img')
                for img in  imgs:
                    src = img.get('src')
                    imgname = ("File:"+(src.lower()).replace("_"," ")).decode('utf-8')
                    if imgname in articledict['Images'].keys():
                        src_fullurl = articledict['Images'][imgname]
                    else: #NOT found in articledict["Images"] keys - search using mw_img_url
                        src_fullurl  = mw_img_url(site, src) # find url of image

                    img.set('src', src_fullurl)

                # wiki remote images: convert <a> to <img>
                links = page_content.findall('.//a')
                for link in  links:                
                    replace_img_a_tag(link)                


                figures = page_tree.findall('.//figure')
                for figure in figures:
                    img = figure.find('.//img')            
                    figcaption = figure.find('.//figcaption')
                    if figcaption is not None:
                        figcaption_text = figcaption.text.upper()

                        # this line gave an error for issue 3 ... :
                        
                        # if figcaption_text in img.get('src').upper():
                            #print 'figcation RM:', figcaption.text, figcaption, ET.tostring(figcaption) 
                            # figure.remove(figcaption)                 


                if mode is 'index':            
                    work_filename = '{}/articles/{}.html'.format(wd, articledict['Title'].replace(' ', '_'))
                elif mode is 'preview':
                    work_filename = '{}/preview/{}.html'.format(wd, articledict['Title'].replace(' ', '_'))

                articledict['Path'] = work_filename.replace(wd+'/', '')        
                write_html_file(page_tree, work_filename)
                #print 'write file', work_filename
                indexdict[articledict['Title']] = articledict
    			#articledict['Path'] = articledict['Path'].replace(wd,'')


    return indexdict
        

def create_index(indexdict, issues):
    issues_keys = issues.keys()
    issues_keys.reverse()
    for issue in issues_keys:
        index_template_file = issue_templates[issue]['index']
        print 
        print index_template_file
        print 
        index_template = open("{}/{}".format(dir_templates, index_template_file), "r") 
        index_tree = html5lib.parse(index_template, namespaceHTMLElements=False)
        
        issueItem=index_tree.find('.//div[@class="issueItem"]')
        # create a section (div.issueItem) for issue articles 
        # in file index-template file

        #print issue_names[issue], issue

        # ET = XML python library
        subissueDiv = ET.SubElement(issueItem, 'div', attrib={'class':'issue'})
        subissueDiv_p = ET.SubElement(subissueDiv, 'p')
        subissueDiv_p.text = "Issue {}: {}".format(issue, issue_names[issue])
        ul_imgNav = ET.SubElement(issueItem, 'ul',
                                  attrib={'class':'imageNavigation',
                                          'style':'"display: none; position: relative; height: 250px;"'})
        
        # here again the sections are hardcoded
        ET.SubElement(issueItem, 'ul',attrib={'class':'list', 'id':'section_Introduction'})
        ET.SubElement(issueItem, 'ul',attrib={'class':'list', 'id':'section_Discourse'})
        ET.SubElement(issueItem, 'ul',attrib={'class':'list', 'id':'section_Projects'})
        ET.SubElement(issueItem, 'ul',attrib={'class':'list', 'id':'section_Proposals'})
        ET.SubElement(issueItem, 'ul',attrib={'class':'list', 'id':'section_Methods'})
        
        # ATTENTION: ids are duplicated in //div#issue_N/ul#section_X
        # ul#section_X = ul#section_Introduction, ul#section_...
        # these <ul>s with same appear more than once. one for each item 
        # change ul.list css to ul.section_Proposals, ul.section_...



    # create an list (both in text & img navigation) item for each article
    # under the parent issue
    # in file index-template.html

    
        for article in indexdict.keys():
            article_issue = indexdict[article]['Category Issue']
            article_issue_numb = article_issue[0]
            print 'ISSUE',article_issue_numb, article_issue[0]

            
            if article_issue_numb == issue: #so that articles from issue N are only listed in index N

                authors = indexdict[article]['Authors']
                path = (indexdict[article]['Path'])
                section = indexdict[article]['Category Section']
                topics =  indexdict[article]['Category Topics']
                images = indexdict[article]['Images']
                index_section = index_tree.find('.//div[@class="issueItem"]/ul[@id="section_{}"]'.format(section.encode('utf-8')))
                index_imgs_section = index_tree.find('.//div[@class="issueItem"]/ul[@class="imageNavigation"]')
                print 'Index Section', ET.tostring(index_section)

                index_item = ET.SubElement(index_section, 'li',
                                           attrib={'class': " ".join(topics)+" "+section,
                                                   'data-name': article,
                                                   'data-section':section,
                                                   'data-categories': " ".join(topics)+" "+section
                                               })
                article_link = ET.SubElement(index_item, 'a', attrib={'href':urllib.quote(path)})
                article_link.text = article
                article_author = ET.SubElement(index_item, 'p', attrib={'class':'authorTitle'})
                article_author.text = authors

                # what is the parent on index_img_section

                # another loop for the visual index
                for imgurl in images.values():
                    index_img_item = ET.SubElement(index_imgs_section, 'li',
                                               attrib={'class': " ".join(topics)+" "+section,
                                                       'data-name': article,
                                                       'data-section':section,
                                                       'data-categories': " ".join(topics)+" "+section,
                                                       'style':'position: absolute; left: 0px; top: 0px;'
                                                   })
                    article_img_link = ET.SubElement(index_img_item, 'a', attrib={'href':urllib.quote(path)})
                    article_img_img = ET.SubElement(article_img_link, 'img', attrib={'src':imgurl})

                title=index_tree.find('.//title')
                title.text = 'Beyond Social: ' + article_issue_numb 
                index_filename = '{}/issue-{}.html'.format(wd, article_issue_numb)
                write_html_file(index_tree, index_filename)


#####
# ACTION
# #####    
site = mwsite(args.host, args.path)
print site

if args.preview is not None:
    #print "** Page Preview Mode**"
    memberpages = [args.preview.encode('utf-8')]
    #print 'memberpages:', memberpages

    #'index' = mode, and if index is set as preview, the output is written to 'preview'
    create_page(memberpages, 'preview')
    
else:
    #print "** New Index Mode **"

    # site is the Site objects
    # args is here reading the args.category to only query the articles with the category "04 Publish Me"
    memberpages = mw_cats(site, args) 
    #print 'memberpages:', memberpages

    #memberpages = a list of all the page names that are categerized under "04 Publish Me"
    #'index' = mode, and if index is set as mode, the output is written to 'articles'
    # indexdict contains a dict for every page, containing all the elements
    indexdict = create_page(memberpages, 'index') 
    #print 'INDEXDICT >>>'
    #pprint.pprint(indexdict)

    create_index(indexdict, issue_names)


