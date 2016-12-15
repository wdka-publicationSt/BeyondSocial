# Beyond Social: converting wiki pages to HTML front-end pages
* Front end link: <http://beyond-social.org/>
* Wiki Link: <http://beyond-social.org/wiki>

Learn more about the process of creating Beyond Social in article [Making Beyond Social](http://beyond-social.org/articles/Making_Beyond_Social.html) 

## Clone Repository
git clone https://github.com/wdka-publicationSt/BeyondSocial.git

## Requirements
* pandoc
* python mwclient https://github.com/mwclient/mwclient 
   * install$ sudo pip install mwclient

## Run
`./bs_wiki2web.py --local` will update the articles in "04_Publish_Me" category.

`./bs_wiki2web.py --local --category "Issue_3" --category "04 Publish Me" ` will update the articles in both "Issue_3" and "04 Publish Me"




