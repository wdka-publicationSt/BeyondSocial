#!/usr/bin/env python
import subprocess, shlex
from argparse import ArgumentParser

wd = '/home/andre/Documents/WdKA/BeyondSocial/development' #working directiory

# arg
# subprocess
# pandoc
# write


p = ArgumentParser()
p.add_argument("--text", default="==test this==[http://beyond-social.org/wiki/index.php/Lexicon Lexicon]")
args = p.parse_args()


def pandoc2html(mw_content):
    '''convert individual mw sections to html'''
    mw_content = mw_content.encode('utf-8')
    tmpfile = open('{}/tmp_content.mw'.format(wd), 'w')
    tmpfile.write(mw_content)
    tmpfile.close()
    args_pandoc = shlex.split( 'pandoc -f mediawiki -t html5 tmp_content.mw' )
    pandoc = subprocess.Popen(args_pandoc, stdout=subprocess.PIPE)
    html = pandoc.communicate()[0]
    html = html.decode("utf-8")
    return html

html=pandoc2html(args.text)
print html
testfile = open('{}/preview/foo.html'.format(wd), 'w')
testfile.write(html)
testfile.close()
