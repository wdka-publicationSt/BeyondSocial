#! /usr/bin/env python
# -*- coding: utf-8 -*-
#################
##  imported by mediawiki.py 
##  MODIFY THE HTML OUTPUT TO BE DISPLAYED IN THE BROWSER
###########
from xml.etree import ElementTree as ET
import urllib2, json, html5lib, sys, re
import pprint

sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://beyond-social.org/wiki/api.php?format=json&"
regex_img = re.compile("http[s]?://.*[\.jpg,\.png,\.gif,\.jpeg]", re.I)

def api_file_url(filename, api_endpoint): # get full urls
    filename = filename.replace(' ', '_')
    query =  "action=query&titles=File:{}&prop=imageinfo&iiprop=url".format(filename)
    url = api_endpoint + query
#    print 'url', url
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    json_dic= ((jsonp.get('query').get('pages')))
#    pprint.pprint(json_dic, indent=2)
    page_id =  json_dic.keys()[0]
#    print 'page_id', page_id
    if int(page_id) != -1: # if ID -1 file does not exist, Meaning: full url already in article  
        imageinfo = (json_dic.get(page_id).get('imageinfo'))[0]
#        print 'imageinfo', imageinfo
        page_url = (json_dic.get(page_id).get('imageinfo'))[0].get('url')
        return page_url 
    else:
        return None


def video_tag(url, extension):
    tag = '''<video controls="controls" preload="metadata" width="100%"> 
        <source src="{src}" type="video/{ext}" />
        </video>'''.format(src=url, ext=extension)
    return ET.fromstring(tag)


def replace_img(parent):
    img = parent.findall('.//figure/img')[0]
    src = img.get('src')
    fileurl = api_file_url(src, endpoint)# find url of file
    if fileurl != None:            
        print 'fileurl', fileurl
        img.set('src', fileurl)

def replace_youtube(parent): 
    youtube = parent.findall('.//youtube')[0]
    youtube_id = youtube.text
    youtube.text=""
    youtube_url = "http://www.youtube.com/embed/{}".format(youtube_id)
    ET.SubElement(parent, 'iframe', {"width":"560", "height":"315", "frameborder": "0", "allowfullscreen": "allowfullscreen", "src": youtube_url})
    parent.remove(youtube)

def replace_anchor_img(parent):
    for anchor in parent.findall('.//a'):
        if re.findall(regex_img, anchor.text):
            parent.remove(anchor)
            figure = ET.SubElement(parent, 'figure', {"id":"test"}) 
            ET.SubElement(figure, 'img', {"src": anchor.text } )




def replace_av(parent):    
    for figure in parent.findall('.//figure'):
        if figure.findall('.//embed'):
            print 'figure', ET.tostring(figure)
            embed=figure.findall('.//embed')[0]
            src = embed.get('src')
            extension = (src.split("."))[-1]
            fileurl = api_file_url(src, endpoint)# find url of file
            title = embed.get('tilte')

            if extension in ['mp4', 'ogv', 'webm']:
                video = ET.SubElement(parent, 'video', {"controls":"controls", "preload": "metadata", "width": "100%", "src": fileurl} ) 
                paragraph = ET.SubElement(parent, 'p', {"class": "av"})
                link = ET.SubElement(paragraph, 'a',  {"href":fileurl} ) 
                link.text = "Download video"

            elif extension in ['mp3', 'ogg']:
                audio = ET.SubElement(parent, 'audio', {"controls":"controls", "preload": "metadata", "width": "100%", "src": fileurl} ) 
                paragraph = ET.SubElement(parent, 'p', {"class": "av"})
                link = ET.SubElement(paragraph, 'a',  {"href":fileurl} ) 
                link.text = "Download audio"

            parent.remove(figure)


def edit_article( article_path ): 
    htmlfile = open(article_path, 'r') 
    tree = html5lib.parse(htmlfile, namespaceHTMLElements=False)
    #print ET.tostring(tree)
    content = tree.findall('.//div[@class="content"]')[0]
    for figure in content.findall('.//figure'):
        if figure.findall('.//img'):
            replace_img(content)
        elif figure.findall('.//embed'):
            print 'embed found'
            replace_av(content)
                    
    for p in content.findall('.//p'): 
        if p.findall('.//youtube'):
            print 'youtube found'
            replace_youtube(p)
        if p.findall('.//a'): # EXTERNAL IMAGES
            replace_anchor_img(p)
                
    # WRITE FILE
    doctype = "<!DOCTYPE html>"
    html = doctype + ET.tostring(tree,  encoding='utf-8', method='html')
    edited = open(article_path, 'w') #write
    print edited
    edited.write(html)
    edited.close()



def edit_html_media(page, api_endpoint, output_filename): #(pagename)
    tree = html5lib.parse(page, namespaceHTMLElements=False)
    for img in tree.findall('.//img'): # images
        src = img.get('src')
        url = api_file_url(src, api_endpoint)# find url of file
        img.set('src', url)
    for p in tree.findall('.//p'): # youtube       
        for child in list(p):
            if child.tag == 'youtube':
                print '---- ---- youtube  ---- ----'
                print  ET.tostring(child)
                print
                youtube_id = child.text
                youtube_url = "http://www.youtube.com/embed/{}".format(youtube_id)
                ET.SubElement(p, 'iframe', 
                              {"width":"560", "height":"315", "frameborder": "0", "allowfullscreen": "allowfullscreen", "src": youtube_url})
    # WRITE FILE
    doctype = "<!DOCTYPE HTML>"
    html = doctype + ET.tostring(tree,  encoding='utf-8', method='html')
    edited = open('html_articles/' + output_filename, 'w') #write
    edited.write(html)
    edited.close()


line = sys.stdin.read()
print line
article = ("articles/{}".format(line) ).replace("\n", "")
print article
edit_article(article)
