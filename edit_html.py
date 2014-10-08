#! /usr/bin/env python
# -*- coding: utf-8 -*-
#################
##  imported by mediawiki.py 
##  MODIFY THE HTML OUTPUT TO BE DISPLAYED IN THE BROWSER
###########
from xml.etree import ElementTree as ET
import urllib2, json, html5lib


def api_file_url(filename, api_endpoint): # get full urls
    filename = filename.replace(' ', '_')
    query =  "action=query&titles=File:{}&prop=imageinfo&iiprop=url".format(filename)
    url = api_endpoint + query
    print 'file:',  url
    request = urllib2.urlopen(url)
    jsonp = json.loads(request.read())    
    json_dic= ((jsonp.get('query').get('pages')))
    page_id =  json_dic.keys()[0]
    page_url = (json_dic.get(page_id).get('imageinfo'))[0].get('url')
    print 'page_url', page_url        
    return page_url 


def edit_html_media(page, api_endpoint, output_filename): #(pagename)
    tree = html5lib.parse(page, namespaceHTMLElements=False)
    print
    print '---- ---- edit_html_media  ---- ----'
    for img in tree.findall('.//img'): # images
        src = img.get('src')
        url = api_file_url(src, api_endpoint)# find url of file
        img.set('src', url)
        print 'IMG', ET.tostring(img)
        print
    for p in tree.findall('.//p'): # youtube       
        for child in list(p):
            if child.tag == 'youtube':
                print '---- ---- youtube  ---- ----'
                print  ET.tostring(child)
                print
                youtube_id= child.text
                embed = '<iframe width="560" height="315" frameborder="0" allowfullscreen="allowfullscreen" src="http://www.youtube.com/embed/{video_id}"/>'.format(video_id=youtube_id)
                embed_element = ET.fromstring(embed)
                p.append(embed_element)
                p.remove(child)
    print '---- ---- END: edit_html_media  ---- ----'
    print

#    for figure in tree.findall('.//figure'): #'.//figure/embed/
#         for element in list(figure):
#             if element.tag == 'embed':
#                 src = element.get('src')
#                 ext = os.path.splitext(src)[1][1:]
#                 url = api_file_url(src)# find url of file
#                 caption = figure.find('.//figcaption')
#                 caption_text = caption.text
#                 av_tag = '''<div class="{medium}">
# '<{medium} src="{src}" controls="controls">
# Sorry, your browser does not support embedded videos. You can download it from <a href="{src}">{src}</a>
# </{medium}>
# <figcaption>{caption}</figcaption>
# </div>'''
#                 # if video or audio
#                 if ext in ['ogv', 'mp4', 'webm'] :                    
#                     av = av_tag.format(src=url, caption=caption_text, medium="video")
#                 elif ext in ['ogg', 'mp3']:                     
#                     av = av_tag.format(src=url, caption=caption_text, medium="audio")

#                 av = ET.fromstring(av)
#                 figure.clear()
#                 figure.extend(av)

    # WRITE FILE
    doctype = "<!DOCTYPE html>"
    html = doctype + ET.tostring(tree,  encoding='utf-8', method='html')
    edited = open(output_filename, 'w') #write
    edited.write(html)
    edited.close()
#    tree.write('htmlpage.html', encoding='utf-8', )
