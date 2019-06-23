#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
## 西门吹雪个人网盘专下工具
    西门吹雪个人网盘地址:
    http://pan.ximcx.cn/home
    此个人网盘收录了很多安全相关的工具,数量较多,下载比较麻烦,因此该工具因势而生,加快下载速度.


## 使用前提:
    1、安装python 2.7
    2、操作系统安装wget

## 使用命令:

    python ximcxdm.py url dir
    其中
    1、ximcxdm.py 即本脚本
    2、url 下载的起始URL,本工具支持子目录下载
    3、dir 本地存放目录,建议空间大一些.

## 使用举例:
    整站:
    python ./ximcxdm.py http://pan.ximcx.cn/home/ ./tmp

    仅下载某一目录,比如渗透测试工具.
    python ./ximcxdm.py http://pan.ximcx.cn/home/home/渗透测试工具 ./tmp

## 工具版本:
    2019-06-23 v0.2 增加含特殊字符&/(/)/等目录的处理
    2019-06-22 v0.1

## 作者
    sy.z

"""
import os
import sys
import time
import getopt
import urllib2
import subprocess
from bs4 import BeautifulSoup

#
# 支持代理 
#
def download_by_urllib2_proxy(ip,port,url,timeout):
    
    proxydict['http'] = "http://%s:%s"%(ip,port)
    # print proxydict
    
    proxy_handler = urllib2.ProxyHandler(proxydict)
    
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)
    try:
        response = urllib2.urlopen(url,timeout=timeout)
        # print response.geturl()
        # print response.getcode()
        # print response.info()
        return response.read()
    except:
        print 'some errors occored' + '-'*50
        return ''


def download_by_urllib2(url,timeout):
    proxydict = {}
    
    proxy_handler = urllib2.ProxyHandler(proxydict)
    
    opener = urllib2.build_opener(proxy_handler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib2.install_opener(opener)
    try:
        response = urllib2.urlopen(url,timeout=timeout)
        # print response.geturl()
        # print response.getcode()
        # print response.info()
        return response.read()
    except:
        print 'some errors occored' + '-'*50
        return ''


# url 下载url
# adir 绝对路径
# 用于下载文件
def download_by_cmd(url, adir):
    print '[FILE] \033[32m' + urllib2.unquote(str(url)) + '\033[0m downloading ...'
    cmd = 'wget -q --show-progress -P "' + adir + '" ' + url 
    subprocess.call(cmd, shell=True)

# url 下载url
# dir 相对路径
# 下载页面和创建本地文件目录
def download(url,dir):

    # print '[DIR] Downloading file to \033[31m'+ dir.encode('utf-8') +'\033[0m, url is \033[33m' + urllib2.unquote(str(url)) + '\033[0m ...'
    print '[DIR] Downloading file to \033[31m'+ dir.encode('utf-8') +'\033[0m, url is \033[33m' + urllib2.unquote(str(url)) + '\033[0m ...'
    #print 'Downloading file to  %s, url is %s ....'  %(dir , unqurl) 
    # 创建文件
    subprocess.call('mkdir -p "' + dir +'"', shell=True)

    #下载README.MD文件
    download_by_cmd( url + '/README.MD', dir)

    # 获取html页面
    timeout = 4
    html = download_by_urllib2(url,timeout)
    
    # print html
    soup = BeautifulSoup(html,'html.parser')

    alllis = soup.findAll('li',{'class':'list-group-item list-group-item-action'});
    for li in alllis:
        col4s = li.findAll('div',{'class':'col-4 col-sm-2'})
        for col4 in col4s:
            link = col4.a
            if link.i['class'][1] == 'fa-download':
                # print link.i['title']
                # print link['href']
                # link[‘href’]是quote过的字符串,带百分号%的.例如 http://pan.ximcx.cn/down/%E6%B8%97%E9%80%8F%E6%B5%8B%E8%AF%95%E5%B7%A5%E5%85%B7/%E6%89%AB%E6%8F%8F%26%E7%88%86%E7%A0%B4/20190402%E5%BE%A1%E5%89%91%E9%AB%98%E9%80%9F%E7%AB%AF%E5%8F%A3%E6%89%AB%E6%8F%8F%E5%B7%A5%E5%85%B7beta.zip
                # 想要获得对应的中文内容，则需要：
                # 1.先去把当前的unicode字符串转换为普通的str
                #  quotedStringStrType= str(quotedStringUnicodeType)
                # 2.再去通过urllib.unquote去解码，得到真正的中文内容
                #  urlunquotedOriginalStr = urllib.unquote(quotedStringStrType); 
                # 然后再输出,注意：此处的最终解码得到的字符串是UTF-8编码的。
                # print urllib2.unquote(str(link['href']))
                download_by_cmd(link['href'],dir)
            
            if link.i['class'][1] == 'fa-folder-open':
                time.sleep(5)
                print '=============== sleep 5s ================='
                download(link['href'], dir + '/' + link['title'])

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    #for arg in args:
    print args
    download(args[0],args[1].decode('utf-8')) # process() is defined elsewhere

if __name__ == "__main__":
    main()
