#! /usr/bin/env python
# -*- coding: utf-8 -*-
#################
##  MODIFY THE HTML OUTPUT TO BE DISPLAYED IN THE BROWSER
###########
from xml.etree import ElementTree as ET
import urllib2, json, html5lib, sys, re, httplib

sid = '1234'
useragent = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
endpoint = "http://beyond-social.org/wiki/api.php?format=json&"
regex_img = re.compile("http[s]?://.*\.(jpg|png|gif|jpeg)", re.I)


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


def replace_img_url(parent):
    extensions_to_check = ['.jpg','.jpeg','.JPG','.JPEG','.png','.gif']
    imgs = parent.findall('.//img')
    captions = parent.findall('.//figcaption')
    for img in imgs:
        src = img.get('src')
        fileurl = api_file_url(src, endpoint)# find url of file
        if fileurl != None:            
            img.set('src', fileurl)

    for caption in captions:
        for ext in extensions_to_check:
            if caption.text is not None and ext in caption.text:
                caption.text = ''

def replace_wikilink(link):
    print "link", link
    host = "beyond-social.org"
    path =  "/articles/"+link+".html" 
    found = 0
    url = ""
    connection = httplib.HTTPConnection(host)  ## Make HTTPConnection Object
    connection.request("HEAD", path)
    responseOb = connection.getresponse()      ## Grab HTTPResponse Object                
    if responseOb.status == 200:
        found = 1
        url = "http://beyond-social.org/articles/{}".format(link)
    else:
        found = 0
        url = "http://beyond-social.org/wiki/index.php/{}".format(link)
    return url
    # print url
#    print 'Found', found

        
def replace_youtube(parent, youtube_id): 
    youtube = parent.findall('.//youtube')[0]
    youtube.text=""
    youtube_url = "http://www.youtube.com/embed/{}".format(youtube_id)
    ET.SubElement(parent, 'iframe', {"width":"560", "height":"315", "frameborder": "0", "allowfullscreen": "allowfullscreen", "src": youtube_url})
    parent.remove(youtube)

    
def replace_anchor4fig(parent, child, src, title ):
    parent.remove(child)
    figure = ET.SubElement(parent, 'figure') 
    ET.SubElement(figure, 'img', {"src": src, "title": title } )
    figcation=ET.SubElement(figure, 'figcaption')
    figcation.text = title

    
def wrap_img(parent, child, src, title):
    parent.remove(child)
    figure = ET.SubElement(parent, 'figure') 
    ET.SubElement(figure, 'img', {"src": src, "title": title } )
    figcation=ET.SubElement(parent, 'figcaption')
    figcation.text = title

    
def replace_av(parent, tree):    
    for figure in parent.findall('.//figure'):
        if figure.findall('.//embed'):
#            print 'figure', ET.tostring(figure)
            embed=figure.findall('.//embed')[0]
            src = embed.get('src')
            extension = (src.split("."))[-1]
            fileurl = api_file_url(src, endpoint)# find url of file
            title = embed.get('title')

            if extension in ['mp4', 'ogv', 'webm']:
                div =  ET.SubElement(parent, 'div', {"width": "100%", "class": "av"} ) 
                video = ET.SubElement(div, 'video', {"controls":"controls", "preload": "metadata", "width": "100%", "src": fileurl} ) 
                paragraph = ET.SubElement(div, 'p', {"class": "av"})
                link = ET.SubElement(paragraph, 'a',  {"href":fileurl} ) 
                link.text = "Download video"

            elif extension in ['mp3', 'ogg']:
                div =  ET.SubElement(parent, 'div', {"width": "100%", "class": "av"} ) 
                audio = ET.SubElement(div, 'audio', {"controls":"controls", "preload": "metadata", "width": "100%", "src": fileurl} ) 
                paragraph = ET.SubElement(div, 'p', {"class": "av"})
                link = ET.SubElement(paragraph, 'a',  {"href":fileurl} ) 
                link.text = "Download audio"

            parent.remove(figure)


def edit_article( article_path ): 
    htmlfile = open(article_path, 'r') 
    tree = html5lib.parse(htmlfile, namespaceHTMLElements=False)

    content = tree.findall('.//div[@class="content"]')[0]


    #remove author's name from article
    author = content.findall('.//p')[0] 
    if 'Author:' in author.text:
        author_text = author.text
        author_name = author_text.replace('Author: ', '')
        author.text =  author_name
        author.set('class',  'authorName')
    elif 'Authors:' in author.text:
        author_text = author.text
        author_name = author_text.replace('Authors: ', '')
        author.text =  author_name
        author.set('class',  'authorName')
        

    
    for figure in content.findall('.//figure'):
        if figure.findall('.//img'):            
#            print 'Replacing image'
            replace_img_url(content)
        elif figure.findall('.//embed'):
            replace_av(content, tree)
                    
    for p in content.findall('.//p'): #loop through <p>
        if p.findall('.//img'): # searching for: <img> outside figure
            #print 'IMAGE OUTSIDE FIGURE:', 
            for img in p.findall('.//img'):
                src =  (img).get('src')
                title = 'TEST'# (img).get('title').replace('|thumbnail','')
                wrap_img(p, img, src, title)
            
        elif p.findall('.//youtube'): # searching for: <youtube>
            youtube_id = (p.findall('.//youtube')[0]).text
#            print 'youtube found', youtube_id , len(p.findall('.//youtube'))
            replace_youtube(p, youtube_id )

        elif p.findall('.//a'): # # searching for: external images as urls
            for anchor in p.findall('.//a'):
                href = anchor.get('href')
                title = anchor.get('title')
                if title == 'wikilink' and 'Category:' not in href: 
                    href = href.replace(" ", "_")
                    print href
                    full_url = replace_wikilink(href)
                    print full_url
                    anchor.set('href',full_url)
                    # print full_url
                    # print ET.tostring(anchor)#['@title']
                    # print 

                if re.match(regex_img, href):
                    if anchor.text != href and anchor.text is not None:
                        title = anchor.text
                    else:
                        title=""
                    replace_anchor4fig(p, anchor, href, title)

        elif p.findall('.//a'): # searching for: <youtube>
            for wikilink in p.findall('.//a'):                
                print "WIKILINK", ET.tostring(wikilink)
                replace_wikilink(wikilink)

                
                    
    # WRITE FILE
    doctype = "<!DOCTYPE html>"
    html = doctype + ET.tostring(tree,  encoding='utf-8', method='html')
    edited = open(article_path, 'w') #write
#    print edited
    edited.write(html)
    edited.close()


for line in sys.stdin.readlines():
#    print line
    article = (("articles/{}".format(line) ).replace("\n", ""))+".html"
#    print article
    edit_article(article)
