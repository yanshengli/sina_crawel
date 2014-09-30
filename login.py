__author__ = 'lige'
#encoding=utf-8
import ConfigParser
from Fetcher import Fetcher
from fetch_info import fetch_info
from fetch_relation import fetch_relation
from mongodb import mongodb
import re

def config_login():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    email = config.get("account", "email")
    password = config.get("account", "password")
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

    relation_method=fetch_relation(url,method,mongodb)#初始化relation类
    info_page=relation_method.fetch_relation()
    #print info_page
    #info_page='http://weibo.cn/2723178631/profile'

    info=fetch_info(info_page,method,mongodb)#初始化info类,爬出文章
    info.fetch_info()

    pro_page=info_page.replace('profile','info')#爬出个人信息
    id=re.search(r"\d{3,11}", info_page).group()
    profile=info.fetch_profile(pro_page)

    conn=mongodb.get_conn()
    conn=conn.weibo.user_relation
    conn.update({'uid':id},{'$set':{'profile':profile}})

