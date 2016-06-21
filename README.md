# Beyond Social:  from wiki To front-end

## Clone Repository
At the moment we are working with branch v1 of BS https://gitlab.com/Castro0o/beyond-social/tree/v1
clone it with git clone https://gitlab.com/Castro0o/beyond-social.git -b v1

## Requirements
* pandoc
* python mwclient https://github.com/mwclient/mwclient 
   * install$ sudo pip install mwclient
## Run
`./bs_wiki2web.py --local` will update the articles in 04_Publish_Me category.
`./bs_wiki2web.py --local --category "03 Proof Me" --category "04 Publish Me" ` will update the articles in both "03 Proof Me" and "04 Publish Me" categories

## Update index and articles


## scripts

### run

### directories
* `html_articles/`: stores the html articles
* `js/`
* `styles/`

### files
* `index.html`: holds the index
* `index-template.html`: a backup file. A copy of index.html, wich can be overwrite the latter
* `article-template.html` provides an article template to pandoc




## TO DO
* duplicated ids: bs_wiki2web.py line 159
* image captions (like pzi, but also disregarding not only "thumbnail", but dimensions; and working with images in the same line )
* author names - via template

