__author__ = 'LiGe'
#encoding:utf-8
from BeautifulSoup import BeautifulSoup

class fetch_info(object):
    def __init__(self,url=None,method=None):
        self.url=url
        self.method=method
    def fetch_info(self,url=None):
        if url==None:
           url=self.url
        method=self.method
        detailpage=method.fetch(url)
        soup= BeautifulSoup(detailpage)
        infos= soup.findAll('div','c')
        for info in infos:
            info= info.findAll('div')
            for line in info:
                if line.find('span', 'ctt'):
                    if line.find('span', 'cmt'):
                        dispatchs=line.find('span', 'cmt')
                        dispatchs=dispatchs.findAll('a')
                        for dispatch in dispatchs:
                            print '转发url', dispatch.attrs
                            print '转发人', dispatch.text
                    else:
                        counts = line.findAll('a')
                        for count in counts:
                            if count.text.find('@') >= 0:
                                print count.attrs
                                print count.text
                    line = line.text.replace('&nbsp;', '')
                    print line
                    continue
                else:
                    if line.find('img'):
                        continue
                    else:
                        lines = line.findAll('a')
                        for line in lines:
                            line = line.text.replace('&nbsp;', ' ')
                            print line
                            continue
    def fetch_profile(self,url=None):
        if url==None:
           url=self.url
        method=self.method
        detailpage=method.fetch(url)
        soup= BeautifulSoup(detailpage)
        profiles=soup.findAll('div', 'c')
        for profile in profiles:
            print profile.text
