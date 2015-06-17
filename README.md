# Beyond Social:  from wiki To front-end

## clone this git
`git clone https://gitlab.com/Castro0o/beyond-social.git`
Files will be kept inside beyond-social.org/html/beyond-social

You can now make git pull from within beyond-social.org/html/beyond-social to keep your cloned repository updated. 
@Template: You cannot do `git push` from the server, only from you own machine!

The workflow shall be:
* Work on you local machine
* Push from local machine to Gitlab
* In the server: Pull updates 

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

