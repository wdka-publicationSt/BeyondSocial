#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import html5lib, urllib, pprint
from bs_modules import pandoc2html, write_html_file, mw_cats, mw_page_imgsurl, mw_img_url, mw_page_text, mwsite, mw_page_cats, mw_page, remove_cats, find_authors, replace_video, replace_img_a_tag, wd
# unsued from bs_modules: replace_gallery, replace_video, index_addwork,
from argparse import ArgumentParser

##############
# REQUIRES: defining wd in bs_modules.py with the full path of BS scripts dir
# chmod a+w tmp_content.mw preview/
#############

#####
# BS topics, section, issue names:
####
category_topic = ['Aesthetics', 'Bottom-up', 'Economics', 'Failures', 'Participation', 'Politics', 'Strategies', 'Transformation', 'Visions', 'Technology']
category_section = ['Discourse', 'Introduction', 'Projects', 'Proposals' ]
issue_names = {'1': 'Redesigning Business'} 
issue_current = issue_names[issue_names.keys()[-1]]

#####
# Args
####
p = ArgumentParser()
p.add_argument('-V', '--version', action='version', version='version 1.0')
p.add_argument("--host", default="beyond-social.org")
p.add_argument("--path", default="/wiki/", help="path: should end with /")
p.add_argument("--category", "-c", nargs="*", default=[['04 Publish Me']], action="append", help="Category to query. Use: -c foo -c bar to intersect multiple categories")
p.add_argument("--preview", help='Preview page. Will override category querying. Use: --page "Name Of Wiki Page"')
#p.add_argument("--preview", action='store_true', help='Preview mode flag. Requires --page "Name Of Wiki Page" ') 
args = p.parse_args()
#print 'args', args

######
# DEFS:  create_page create_index
######
def create_page(memberpages, mode):
    page_template = open("{}/article-template.html".format(wd), "r")
    indexdict = {} #parent dict: contains articledict instances
    for member in memberpages:
        #print member
        page = mw_page(site, member)
        page_cats = mw_page_cats(site, page)
        page_text = mw_page_text(site, page)
        page_imgs = mw_page_imgsurl(site, page)
        page_imgs = { key.capitalize():value for key, value in page_imgs.items()} # capatalize keys, so can be called later
        articledict = {'Title': member, 'Content': page_text, 'Categories':page_cats, 'Images': page_imgs}

        if articledict['Content']:# clean and convert content to html
            articledict['Authors'], articledict['Content'] = find_authors(articledict['Content'])
            articledict['Content'] = remove_cats(articledict['Content'])
            articledict['Content'] = replace_video(articledict['Content'])
            articledict['Content'] = pandoc2html(articledict['Content'])
            articledict['Category Topics'] = [] #as to be appended in loop below
            
            for entry in articledict['Categories']:
                category =  (entry).replace('Category:', '')
                if 'Issue' in category:
                    articledict['Category Issue'] = category.replace('Issue ','')
                    articledict['Category Issue'] = articledict['Category Issue']  +' '+ issue_names[articledict['Category Issue']]
                elif category in category_topic:
                    articledict['Category Topics'].append(category)
                elif category in category_section:
                    articledict['Category Section']= category
            articledict.pop('Categories') 

            # HTML tree  # create work page
            page_tree = html5lib.parse(page_template, namespaceHTMLElements=False)
            page_title = page_tree.find('.//title')
            page_title_h1 = page_tree.find('.//h1[@title="title"]')
            page_title.text = articledict['Title']
            page_title_h1.text = articledict['Title']
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
                
            if mode is 'index':            
                work_filename = '{}/articles/{}.html'.format(wd, articledict['Title'].replace(' ', '_'))
            elif mode is 'preview':
                work_filename = '{}/preview/{}.html'.format(wd, articledict['Title'].replace(' ', '_'))

            articledict['Path'] = work_filename        
            write_html_file(page_tree, work_filename)
            #print 'write file', work_filename
            indexdict[articledict['Title']] = articledict
            
    return indexdict
        

def create_index(indexdict):
    index_template = open("{}/index-template.html".format(wd), "r") 
    index_tree = html5lib.parse(index_template, namespaceHTMLElements=False)
    index_imgs_section = index_tree.find('.//ul[@class="imageNavigation"]')
    
    for article in indexdict.keys():    
        authors = indexdict[article]['Authors']
        path = (indexdict[article]['Path'])
        issue = indexdict[article]['Category Issue']
        section = indexdict[article]['Category Section']
        topics =  indexdict[article]['Category Topics']
        images = indexdict[article]['Images']
        index_section = index_tree.find('.//ul[@id="section_{}"]'.format(section.encode('utf-8')))
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
    title.text = 'Beyond Social: ' + issue_current
    index_filename = '{}/index.html'.format(wd)
    write_html_file(index_tree, index_filename)


#####
# ACTION
#####    
site = mwsite(args.host, args.path)

if args.preview is not None:
    #print "** Page Preview Mode**"
    memberpages = [args.preview.encode('utf-8')]
    #print 'memberpages:', memberpages
    create_page(memberpages, 'preview')
    
else:
    #print "** New Index Mode **"
    memberpages=mw_cats(site, args)
    #print 'memberpages:', memberpages
    indexdict = create_page(memberpages, 'index')
    #pprint.pprint(indexdict)
    create_index(indexdict)


