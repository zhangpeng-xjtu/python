#!/usr/bin/python
#encoding:utf-8

import re
import urllib
import os
import shutil

def getHtml(url):
    url = re.sub(r'\s', '', url)
    if not url.startswith('http'):
        url = 'http://' + url

    response = urllib.urlopen(url)
    return response.read()

def parseImgs(html):
    if len(html) <= 0:
        return []

    reg = re.compile(r'src=["\']([^"\']*(jpg|png))["\']', re.M | re.I)
    imgs = re.findall(reg, html)
    ret = []
    dup = {}
    for img in imgs:
        if dup.has_key(img[0]):
            continue
        dup[img[0]] = True

        if img[0].startswith('http'):
            ret.append(img)
        else:
            ret.append(['http://' + img[0], img[1]])

    return ret

def downloadImgs(imgs):
    try:
        shutil.rmtree('img')
    except:
        print 'rm img folder failed'

    os.mkdir('img')
    index = 0
    for img in imgs:
        try:
            index += 1
            print 'download: %s' % img[0]
            urllib.urlretrieve(img[0], 'img/%d.%s' % (index, img[1]))
        except:
            print 'download %s failed' % img[0]

html = getHtml('http://news.baidu.com')
print html
imgs = parseImgs(html)
downloadImgs(imgs)