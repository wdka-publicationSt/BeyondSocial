from __main__ import *
import pprint, re, subprocess, shlex, os
import xml.etree.ElementTree as ET
from mwclient import Site


#########
# Site Level
#########
def mwsite(host, path): #returns wiki site object
    site = Site(host, path)
    return site

def mw_cats(site, args): #returns pages member of args(categories)
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

    

##############################
# CATEGORIES, PAGES AND IMAGES
##############################
def mw_page(site, page):
    page = site.Pages[page]
    return page

def mw_page_text(site, page):
    text = page.text()
    return text

def mw_page_cats(site, page):
    cats_list = list(page.categories())
    cats = [cat.name for cat in cats_list if cat.name != u'Category:04 Publish Me'] 
    return cats


def mw_page_imgsurl(site, page):
    #all the imgs in a page
    #returns list of tuples (img.name, img.fullurl)
    imgs = page.images()
    imgs = list(imgs)
    urls = { img.name: (img.imageinfo)['url'] for img in imgs}
    return urls


def mw_img_url(site, img): #find full of an img 
    if 'File:' not in img:
        img = 'File:'+img
    img_page=site.Pages[img]
    img_url = (img_page.imageinfo)['url']
    return img_url




# PROCESSING MODULES

def write_html_file(html_tree, filename):
    doctype = "<!DOCTYPE HTML>"
    html = doctype + ET.tostring(html_tree,  method='html', encoding='utf-8', ) 

    basename = os.path.basename(filename) 
    directory = filename.replace(basename, '')
    print 'directory', directory    
    if os.path.isdir(directory) is False:
        os.makedirs(directory)        
    edited = open(filename, 'w') #write
    edited.write(html)
    edited.close()

def pandoc2html(mw_content):
    '''convert individual mw sections to html'''
    mw_content = mw_content.encode('utf-8')
    tmpfile = open('{}/tmp_content.mw'.format(wd), 'w')
    tmpfile.write(mw_content)
    tmpfile.close()
    args_pandoc = shlex.split( 'pandoc -f mediawiki -t html5 {}/tmp_content.mw'.format(wd) )
    pandoc = subprocess.Popen(args_pandoc, stdout=subprocess.PIPE)
    html = pandoc.communicate()[0]
    html = html.decode("utf-8")
    return html

author_exp = re.compile('^Authors?\: ?(.*?)\\n')
cat_exp = re.compile('\[\[Category\:.*?\]\]')
gallery_exp=re.compile('<gallery>(.*?)</gallery>', re.S)
imgfile_exp=re.compile('(File:(.*?)\.(gif|jpg|jpeg|png))')

def find_authors(content):
    authors = re.findall(author_exp, content[0:100]) #search only in 1st lines
    if authors:
        #replace authors in content
        content = re.sub(author_exp, '', content)
        authors = authors[0]        
    else:
        content = content
        authors = None
    return (authors, content) 
    
def remove_cats(content):
    content = re.sub(cat_exp, '', content)
    return content
    print 'NO CATS', content

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

img_exp=re.compile('^.*?\.(?:jpg|jpeg|JPG|JPEG|png|gif)')

def replace_img_a_tag(img_anchor):
    # TO DO: remove <a> - requires finding the img_anchor
    href = img_anchor.get('href')
    if re.match(img_exp, href):
        img_anchor.clear()
        figure = ET.SubElement(img_anchor, 'figure')
        img = ET.SubElement(figure, 'img', attrib={'src': href})
#        figcaption = ET.SubElement(figure, 'figcaption')
#        figcaption.text = href



        
