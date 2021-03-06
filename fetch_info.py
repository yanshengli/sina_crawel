__author__ = 'LiGe'
#encoding:utf-8
from BeautifulSoup import BeautifulSoup
import re
from mongodb import mongodb

class fetch_info(object):
    def __init__(self,url=None,method=None, mongodb=None):
        self.url=url
        self.method=method
        self.conn=mongodb
    def fetch_info(self,url=None):
        if url==None:
           url=self.url
        method=self.method
        conn=self.conn.get_conn()
        conn=conn.weibo.user_info
        info_num=0
        while info_num<1 :
            print url
            detailpage=method.fetch(url)
            soup= BeautifulSoup(detailpage)
            infos= soup.findAll('div','c')
            for info in infos:
                info_user=dict()
                #info_user['uid']=re.search(r"\d{3,11}", self.url).group()
                info_user['uid']=self.url.split('/')[3]
                info= info.findAll('div')
                for line in info:
                    if line.find('span', 'ctt'):
                        if line.find('span', 'cmt'):
                            dispatchs=line.find('span', 'cmt')
                            dispatchs=dispatchs.findAll('a')
                            for dispatch in dispatchs:
                                #print '转发url', dispatch.attrs
                                #print '转发人', dispatch.text
                                info_user['转发url']=str(dispatch.attrs[0][1])
                                info_user['转发人']=dispatch.text
                        else:
                            counts = line.findAll('a')
                            for count in counts:
                                if count.text.find('@') >= 0:
                                    #print count.attrs
                                    #print count.text
                                    info_user['@对象url']=str(count.attrs[0][1])
                                    info_user['@对象']=count.text
                        line = line.text.replace('&nbsp;', '')
                        if line.find(u'赞[')>=0 and line.find(u'原文转发[')<0:
                            print line
                            line_num=re.findall(r"\[[0-9]+\]",line)
                            if line_num.__len__()==0:
                                continue
                            info_user['赞数']=line_num[0][1:-1]
                            info_user['转发数']=line_num[1][1:-1]
                            info_user['评论数']=line_num[2][1:-1]
                            start1=line.find(u'收藏')
                            start2=line.find(u'来自')
                            if start1>=0 and start2>=0:
                                info_user['时间']=line[start1+2:start2]
                        info_user['消息']=line
                        continue
                    else:
                        if line.find('img') and line.find(u'原文转发'):
                            continue
                        lines = line.findAll('a')
                        line = line.text.replace('&nbsp;', ' ')
                        start1=line.find(u'收藏')
                        start2=line.find(u'来自')
                        if start1>=0 and start2>=0:
                            info_user['时间']=line[start1+2:start2]
                        for line in lines:
                            line = line.text.replace('&nbsp;', ' ')
                            if line.find(u'赞[')>=0:
                                print line
                                info_user['赞数']=re.search(r"\[[0-9]+\]", line).group()[1:-1]
                            if line.find(u'转发[')>=0:
                                info_user['转发数']=re.search(r"\[[0-9]+\]", line).group()[1:-1]
                            if line.find(u'评论[')>=0:
                                print line
                                info_user['评论数']=re.search(r"\[[0-9]+\]", line).group()[1:-1]
                conn.insert(info_user)
            info_num=info_num+1
            nextpage=soup.find('div', {'class':'pa'}, {'id':'pagelist'})
            if nextpage is None:
                break
            pagetext=nextpage.find('a').text
            if pagetext.find(u'下页')<0:
                break
            else:
                url='http://weibo.cn'+str(nextpage.find('a').attrs[0][1])
                print url

    def fetch_profile(self,url=None):
        if url==None:
           url=self.url
        user_dict=dict()
        #pattern='(&nbsp)|(&gt;)'
        pattern1=ur">([\u4e00-\u9fa5]+):(([\u4e00-\u9fa5_a-zA-Z0-9]+)|(([\u4e00-\u9fa5]+)\s([\u4e00-\u9fa5]+))|(\d{4}-\d{2}-\d{2}))<br"
        method=self.method
        detailpage=method.fetch(url)
        soup= BeautifulSoup(detailpage)
        profiles=soup.findAll('div', 'c')
        for profile in profiles:
            if profile.text.find(u'设置') >= 0:
                break
            if profile.text.find(u'昵称')>=0:
                #print profile
                pattern=re.compile(pattern1)
                user_profile= pattern.findall(str(profile).decode('utf-8'))
                if user_profile is not None:
                    for info in user_profile:
                        user_dict[info[0]]=info[1]
                user_dict['aboutme']=profile.text
        return user_dict


