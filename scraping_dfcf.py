# coding = UTF-8
# 抓取dfcf的研报

import json
import time
import downloader
import pymongo
import urllib.parse
import urllib.request
import os

URL = 'http://app.jg.eastmoney.com/Report/Search.do?securitycodes=000063.SZ&gridTitle=%E4%B8%AD%E5%85%B4%E9%80%9A%E8%AE%AF&cid=4895084926073564&pageIndex=1&limit=50&sort=datetime&order=desc'
client = pymongo.MongoClient('mongodb://localhost:27017')
collections = client['dfcf_pdf'].datalist

D = downloader.Downloader()
result = D(URL)
records = json.loads(result.decode('utf-8')).get('records')

# 插入数据库
def insert_datalist(item):
    if collections.find({'id': item['id']}).count() == 0:
        collections.insert_one(item)
        print('insert Succeed!!!')

def scrap_pdf(delay = 3):
    for item in records:
        pfd_url = item['attach'][0]['url']
        PDF_file_name = 'PDF_file/'

        if os.path.exists(PDF_file_name) == False:
            os.makedirs(PDF_file_name)

        file_name = PDF_file_name + pfd_url.split('/')[-1]
        if os.path.exists(file_name):
            continue
        # 下载pdf文件
        u = urllib.request.urlopen(pfd_url)
        f = open(file_name, 'wb')
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
        # 修改item的url字段改成自己的服务器的地址
        item['attach'][0]['url'] = '/Users/wanglei/PycharmProjects/untitled1/' + file_name
        # 插入到数据库里
        insert_datalist(item)
        # 加个延时 别抓的太快 被封了 苦逼
        time.sleep(delay)

scrap_pdf(3)
