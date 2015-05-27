#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import html5lib, pprint
from bs_modules import pandoc2html, replace_gallery, replace_video, index_addwork, write_html_file, mw_cats, mw_page_imgsurl, mw_img_url, mw_page_text, mwsite, mw_page_cats, mw_page, remove_cats, find_authors
from argparse import ArgumentParser

category_topic = ['Aesthetics', 'Bottom-up', 'Economics', 'Failures', 'Participation', 'Politics', 'Strategies', 'Transformation', 'Visions', 'Technology']
category_section = ['Discourse', 'Introduction', 'Projects', 'Proposals' ]
issue_names = {'1': 'Redesigning Business'} 

p = ArgumentParser()
p.add_argument("--host", default="beyond-social.org")
p.add_argument("--path", default="/wiki/", help="nb: should end with /")
p.add_argument("--category", "-c", nargs="*", default=[['04 Publish Me']], action="append", help="category to query, use -c foo -c bar to intersect multiple categories")
args = p.parse_args()
print args

site = mwsite(args.host, args.path)
memberpages=mw_cats(site, args)
# memberpages = [u'Designing Change'] # for testing
#print 'memberpages', memberpages

########
# Templates
########
page_template = open("article-template.html", "r")
#index_template = open('index-template.html', 'r') 
#index_tree = html5lib.parse(index_template, namespaceHTMLElements=False)
#index_container = index_tree.find(".//div[@class='isotope']") #maybe id is important, to destinguish it


########
# Create Page 
########
for member in memberpages:
    print member
    page = mw_page(site, member)
    page_cats = mw_page_cats(site, page)
    page_text = mw_page_text(site, page)
#    page_imgs = mw_page_imgsurl(site, page)    
    workdict = {'Title': member, 'Content': page_text, 'Categories':page_cats}

    if workdict['Content']:# clean and convert content to html
        workdict['Authors'], workdict['Content'] = find_authors(workdict['Content'])
        workdict['Content'] = remove_cats(workdict['Content'])
        workdict['Content'] = pandoc2html(workdict['Content'])
        workdict['Category Topics'] = [] #as to be appended in loop below
        
        # todo: replace images src with full url # with html
        for entry in workdict['Categories']:
            category =  (entry).replace('Category:', '')
            if 'Issue' in category:
                workdict['Category Issue'] = category.replace('Issue ','')          
                workdict['Category Issue'] = workdict['Category Issue']  +' '+ issue_names[workdict['Category Issue']]                                 
            elif category in category_topic:
                workdict['Category Topics'].append(category)
            elif category in category_section:
                workdict['Category Section']= category
            
        # pprint.pprint(workdict['Category Topics'])
        # pprint.pprint(workdict['Category Issue'])
        # print
        
        # HTML tree
        # create work page
        page_tree = html5lib.parse(page_template, namespaceHTMLElements=False)
        page_title = page_tree.find('.//title')
        page_title_h1 = page_tree.find('.//h1[@title="title"]')
        page_title.text = workdict['Title']
        page_title_h1.text = workdict['Title']
        page_issue =  page_tree.find('.//span[@id="issue"]')
        page_issue.text = workdict['Category Issue']
        page_section = page_tree.find('.//span[@id="section"]')
        page_section.text = workdict['Category Section']
        page_topics =  page_tree.find('.//span[@id="topics"]')
        page_topics.text = " ".join(workdict['Category Topics'])
        
        # maybe this can be MADE + SIMPLY
        # but content comes wrapped in <html><body>
        page_content = page_tree.find('.//div[@class="content"]')
        content =  html5lib.parse(workdict['Content'], namespaceHTMLElements=False)
        bodycontent = content.findall('.//body/*') 
        for el in bodycontent:
            page_content.append(el)

        # imgs full url
        imgs = page_content.findall('.//img')
        for img in  imgs:
            img_fullurl = mw_img_url(site, img.get('src'))
            img.set('src', img_fullurl)
        
#        print ET.tostring(page_tree) 
        work_filename = 'articles/{}.html'.format( workdict['Title'].replace(' ', '_'))
        write_html_file(page_tree, work_filename)


        


        
        
