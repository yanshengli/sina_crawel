__author__ = 'LiGe'
#encoding:utf-8
from BeautifulSoup import BeautifulSoup


class fetch_relation(object):
    def __init__(self,url=None,method=None):
        self.url=url
        self.method=method
    def fetch_relation(self,url=None):
        if url==None:
            url=self.url
        method=self.method
        while True:#获取所有的关注用户
                url=method.fetch(url)
                soup=BeautifulSoup(url)
                soups=soup.findAll('td')
                num=0
                for line in soups:
                    if not line.has_key('style'):
                        num=num+1
                        line1= line.find('a')
                        print line1.text#好友名
                        print line1.attrs#好友url
                nextpage=soup.find('div', {'class': 'pa'}, {'id': 'pagelist'})
                if nextpage is None:
                    break
                else:
                    if nextpage.text.find(u'下页')< 0:
                        break
                print nextpage
                nextpage=nextpage.find('a')
                url='http://weibo.cn'+str(nextpage.attrs[0][1])
        #print num
        count=soup.find('div', 'tip2')
        count=count.findAll('a')
        for line in count:
            if line.text.find(u'微博')>=0:
                url_weibo='http://weibo.cn'+str(line.attrs[0][1])
                print line.text
            if line.text.find(u'粉丝')>=0:
                print line.text
        return url_weibo
