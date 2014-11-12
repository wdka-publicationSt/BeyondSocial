# Beyond Social:  from wiki To front-end

## clone this git
`git clone https://gitlab.com/Castro0o/beyond-social.git`
Files will be kept inside beyond-social/ directory.

**On server:** 
`cd beyond-social.org/html`

Run: `./copy2parentdir.sh` - it will copy the html,js,css to ../beyond-social/


## scripts
Uses the following scripts:
* `edit_index.py` - responsible for updating the index with wiki articles tagged: 04_Publish_Me
* `create_articles.py` - generates the html files mentioned in index

### run
In order to this scripts in complement:

make both scripts executable:

`chmod +x create_articles.py; chmod +x edit_index.py`

pipe the output from on to the other:

`./edit_index.py | ./create_article.py`

the result is an upto date index
and corresping articles

### directories
* `html_articles/`: stores the html articles
* `js/`
* `styles/`
### files
* `index.html`: holds the index
* `index.html.bak`: a backup file. A copy of index.html, wich can be overwrite the latter
* `template_article.html` provides an article template to pandoc



# TODO 
* in `index.html` and `edit_index.py`:
   * replace old topics with current
       * update javascript to work with it
   * Andre: I am confused with in index.html {CATEGORY NAME}
   
* In `./create_article.py` 
   * parse images and av media

