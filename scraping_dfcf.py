# coding = UTF-8
# 抓取dfcf的研报

import json
import downloader
import pymongo
import urllib.parse
import urllib.request
import os

URL = 'http://app.jg.eastmoney.com/Report/Search.do?securitycodes=000063.SZ&gridTitle=%E4%B8%AD%E5%85%B4%E9%80%9A%E8%AE%AF&cid=4895084926073564&pageIndex=1&limit=50&sort=datetime&order=desc'

D = downloader.Downloader()
result = D(URL)
records = json.loads(result.decode('utf-8')).get('records')

index = 0
for item in records:
    if index == 2: break
    pfd_url = item['attach'][0]['url']

    PDF_file_name = 'PDF_file/'
    if os.path.exists(PDF_file_name) == False:
        os.makedirs(PDF_file_name)

    file_name = PDF_file_name + pfd_url.split('/')[-1]
    if os.path.exists(file_name):
        continue

    u = urllib.request.urlopen(pfd_url)
    f = open(file_name, 'wb')
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    item['attach'][0]['url'] = '/Users/wanglei/PycharmProjects/untitled1/' + file_name
    index+=1
    print('\n')

# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client['dfcf_pdf']
# for i in db.datalist.find():
#     print(i)
# print(json.loads(db.datalist.find()))