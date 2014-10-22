__author__ = 'lige'
#encoding=utf-8
import ConfigParser
from Fetcher import Fetcher
from fetch_info import fetch_info
from fetch_relation import fetch_relation
from mongodb import mongodb
from get_follow import get_follow
import time

def config_login():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    email = config.get("account1", "email")
    password = config.get("account1", "password")
    seed=config.get("seed_url", "seed")
    db=config.get('database', 'db')
    collection_info=config.get('collection', 'table_info')
    collection_relation=config.get('collection', 'table_relation')
    method=Fetcher()
    method.login(email, password)
    url=seed
    return url, method, db, collection_info, collection_relation


if __name__ == '__main__':
    url, method, db, collection_info, collection_relation=config_login()
    ip='127.0.0.1'
    port=27017
    mongodb=mongodb(ip,port)
    conn=mongodb.get_conn()

    complete=conn.weibo.completes
    complete_user=complete.find()#建立complete数据库
    users=set()
    for every_complete_user in complete_user:
        users.add(every_complete_user['uid'][1])
    #print users

    relation=conn.weibo.user_relation#建立relation数据库
    posts=relation.find()
    count=posts.count()
    print count

    if users.__len__()==0:
        print url
        follow_method=get_follow(url,method)
        url_follow=follow_method.get_follow()#获取follow的url
        print url_follow
        relation_method=fetch_relation(url_follow,method,mongodb)#初始化relation类
        info_page=relation_method.fetch_relation()
        my_info=('hitwhhw',url)
        info=fetch_info(info_page,method,mongodb)#初始化info类,爬出文章
        info.fetch_info()
        pro_page=info_page.replace('profile','info')#爬出个人信息
        id=info_page.split('/')[3]
        profile=info.fetch_profile(pro_page)
        relation.update({'uid':id},{'$set':{'profile':profile}})#根新个人资料
        temp_user=dict()#加入到已完成的表里
        temp_user['uid']=my_info
        complete.insert(temp_user)
        time.sleep(5)

    for post in posts:
        print 'ok'
        follow_users=post['follow']
        for every_user in follow_users:
            if every_user[1] not in users:
                print every_user[1]
                follow_method=get_follow(every_user[1],method)
                url_follow=follow_method.get_follow()#获取follow的url
                if url_follow==None:
                    print '用户不存在了'
                    continue
                print url_follow
                relation_method=fetch_relation(url_follow,method,mongodb)#初始化relation类
                info_page=relation_method.fetch_relation()
                print info_page
                info=fetch_info(info_page,method,mongodb)#初始化info类,爬出文章
                info.fetch_info()
                pro_page=info_page.replace('profile','info')#爬出个人信息
                print pro_page
                id=info_page.split('/')[3]
                profile=info.fetch_profile(pro_page)
                relation.update({'uid':id},{'$set':{'profile':profile}})#根新个人资料
                temp_user=dict()#加入到已完成的表里
                temp_user['uid']=every_user
                complete.insert(temp_user)
                #time.sleep(5)

