#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pprint, re, subprocess, shlex, urllib
import xml.etree.ElementTree as ET
from mwclient import Site
site = Site("pzwiki.wdka.nl", path="/mw-mediadesign/")

##############################
# CATEGORIES, PAGES AND IMAGES
##############################
def mw_page_text(site, page):
    page = site.Pages[page]
    text = page.text()
    return text

def mw_cats(site, args):
    last_names = None
    for cats in args.category:
            for ci, cname in enumerate(cats):
                    cat = site.Categories[cname]
                    pages = list(cat.members())
                    # for p in pages:
                    # 	pages_by_name[p.name] = p
                    if last_names == None:
                            results = pages
                    else:
                            results = [p for p in pages if p.name in last_names]                
                    last_names = set([p.name for p in pages])
            results = list(results)
    return [p.name  for p in results]

def mw_singelimg_url(site, img): #find full of an img 
    if 'File:' not in img:
        img = 'File:'+img
    img_page=site.Pages[img]
    img_url = (img_page.imageinfo)['url']
    return img_url

def mw_imgsurl(site, page): #all the imgs in a page #return: list of tuples (img.name, img.fullurl)
    page = site.Pages[page]
    imgs = page.images()
    imgs = list(imgs)
    urls = [((img.name),(img.imageinfo)['url']) for img in imgs]
    return urls




# PROCESSING MODULES

def write_html_file(html_tree, filename):
    doctype = "<!DOCTYPE HTML>"
    html = doctype + ET.tostring(html_tree,  method='html', encoding='utf-8', ) 
    edited = open(filename, 'w') #write
    edited.write(html)
    edited.close()

def parse_work(title, content):
    workdict = {'Title':title, 'Creator':u'', 'Date':u'', 'Website':u'', 'Thumbnail':u'', 'Bio':u'', 'Description':u'', 'Extra':u''}    
    if re.match(u'\{\{\Graduation work', content):
        template, extra = (re.findall(u'\{\{Graduation work\n(.*?)\}\}(.*)', content, re.DOTALL))[0]
        if extra:
            workdict['Extra'] = extra
        # template's key/value pair
        # Note:Extra value is NOT CAPTURED by this regex
        keyval = re.findall(u'\|(.*?)\=(.*?\n)', template, re.DOTALL) 
        for pair in keyval:
            key = pair[0]
            val = (pair[1]).replace('\n', '')
            if 'Creator' in key:
                val = val.replace(u', ', u'')
            elif 'Thumbnail' in key:
                val = mw_singelimg_url(site, val)#api_thumb_url(val)
            elif 'Website' in key:
                val = urllib.unquote( val)                
            workdict[key]=val
#    pprint.pprint(workdict)
    return workdict

def pandoc2html(mw_content):
    '''convert individual mw sections to html'''
    mw_content = mw_content.encode('utf-8')
    # convert from mw to html
    args_echo =shlex.split( ('echo "{}"'.format(mw_content)) )
    args_pandoc = shlex.split( 'pandoc -f mediawiki -t html5' )
    p1 = subprocess.Popen(args_echo, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(args_pandoc, stdin=p1.stdout, stdout=subprocess.PIPE)
    html = (p2.communicate())[0]
    html = html.decode("utf-8")
    return html
            
gallery_exp=re.compile('<gallery>(.*?)</gallery>', re.S)
imgfile_exp=re.compile('(File:(.*?)\.(gif|jpg|jpeg|png))')

def replace_gallery(content):
    content = re.sub(imgfile_exp, '[[\g<1>]]', content) #add [[ ]] to File:.*?
    content = re.sub(gallery_exp, '\g<1>', content) #remove gallery wrapper
    return content

video_exp=re.compile('\{\{(.*?)\|(.*?)\}\}')
vimeo_exp=re.compile('\{\{vimeo\|(.*?)\}\}')
youtube_exp=re.compile('\{\{youtube\|(.*?)\}\}')

def replace_video(content):
    content = re.sub(vimeo_exp,"<iframe src='https://player.vimeo.com/video/\g<1>' width='600px' height='450px'> </iframe>", content)
    content = re.sub(youtube_exp, "<iframe src='https://www.youtube.com/embed/\g<1>' width='600px' height='450px'> </iframe>", content)
    return content


# Index Creation
def index_addwork(parent, workid, href, thumbnail, title, creator, date):
    child_div = ET.SubElement(parent, 'div', attrib={'class':'item',
                                                     'id':workid,
                                                     'data-title':title,
                                                     'data-creator':creator,
                                                     'data-date':date})

    grandchild_a = ET.SubElement(child_div, 'a', attrib={'href':href, 'class':'work'})
    if thumbnail is '':
        grandgrandchild_h3 = ET.SubElement(grandchild_a, 'h3', attrib={'class':'work', 'id':'thumbnail_replacement'})
        grandgrandchild_h3.text=title
    else:
        grandgrandchild_img = ET.SubElement(grandchild_a, 'img', attrib={'class':'work', 'src':thumbnail})    
    # need to add css width to div.item
