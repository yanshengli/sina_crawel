__author__ = 'lige'
#encoding=utf-8
import ConfigParser
from Fetcher import Fetcher
from fetch_info import fetch_info
from fetch_relation import fetch_relation

def config_login():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    email = config.get("account", "email")
    password = config.get("account", "password")
    seed=config.get("seed_url", "seed")
    method=Fetcher()
    method.login(email, password)
    url=seed
    return url,method


if __name__=='__main__':
    url,method=config_login()
    relation_method=fetch_relation(url,method)#初始化relation类
    info_page=relation_method.fetch_relation()
    print info_page
    info=fetch_info(info_page,method)#初始化info类,爬出文章
    info.fetch_info()
    pro_page=info_page.replace('profile','info')#爬出个人信息
    print pro_page
    info.fetch_profile(pro_page)
