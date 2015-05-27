#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import html5lib, pprint
from bs_modules import pandoc2html, replace_gallery, replace_video, index_addwork, write_html_file, mw_cats, mw_page_imgsurl, mw_img_url, mw_page_text, mwsite, mw_page_cats, mw_page, remove_cats, find_authors
from argparse import ArgumentParser

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
     #....
     # ....

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

        # todo: replace images src with full url # with html

        pprint.pprint(workdict)
        print



        
        #HTML tree
        page_tree = html5lib.parse(workdict['Content'], namespaceHTMLElements=False)

        # imgs full url
        imgs = page_tree.findall('.//img')
        for img in  imgs:
            img_fullurl = mw_img_url(site, img.get('src'))
            print 'IMG_URL', img_fullurl
            img.set('src', img_fullurl)

    


# # images
# # categories

        
        
