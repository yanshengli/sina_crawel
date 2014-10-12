__author__ = 'LiGe'
#encoding:utf-8
from BeautifulSoup import BeautifulSoup
from mongodb import mongodb
import re
class fetch_relation(object):
    def __init__(self,url=None,method=None ,mongodb=None):
        self.url=url
        self.method=method
        self.conn=mongodb

    def fetch_relation(self,url=None):
        json_user=dict()
        relation_list=list()
        user=tuple()
        conn=self.conn.get_conn()
        dc=conn.weibo.user_relation
        if url==None:
            url=self.url
        method=self.method
        num=0
        while True:#获取所有的关注用户
                url=method.fetch(url)
                soup=BeautifulSoup(url)
                soups=soup.findAll('td')
                for line in soups:
                    if not line.has_key('style'):
                        num=num+1
                        line1= line.find('a')
                        #print line1.text#好友名
                        #print line1.attrs#好友url
                        user=(line1.text, line1.attrs[0][1])
                        relation_list.append(user)
                nextpage=soup.find('div', {'class': 'pa'}, {'id': 'pagelist'})
                if nextpage is None:
                    break
                else:
                    if nextpage.text.find(u'下页')< 0:
                        break
                #print nextpage
                nextpage=nextpage.find('a')
                url='http://weibo.cn'+str(nextpage.attrs[0][1])

        #json_user['uid']=re.search(r"\d{3,11}", self.url).group()
        json_user['uid']=self.url.split('/')[3]
        json_user['follow']=relation_list
        json_user['follow_num']=num

        count=soup.find('div', 'tip2')
        count=count.findAll('a')
        for line in count:
            if line.text.find(u'微博')>=0:
                url_weibo='http://weibo.cn'+str(line.attrs[0][1])
                json_user['微博数']=re.search(r"\d{1,}", line.text).group()
                #print line.text
            if line.text.find(u'粉丝')>=0:
                json_user['粉丝数']=re.search(r"\d{1,}", line.text).group()
                #print line.text
        dc.insert(json_user)
        return url_weibo
