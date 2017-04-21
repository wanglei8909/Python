import urllib.request
import json
import downloader


def download(url, user_agent='WL', num_retries=2):
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.URLError as e:
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries-1)
    return json.loads(html.decode('utf-8')).get('records')
# print(download('http://app.jg.eastmoney.com/Report/Search.do?securitycodes=000063.SZ&gridTitle=%E4%B8%AD%E5%85%B4%E9%80%9A%E8%AE%AF&cid=4895084926073564&pageIndex=1&limit=50&sort=datetime&order=desc'))
# myArray = download('http://app.jg.eastmoney.com/Report/Search.do?securitycodes=000063.SZ&gridTitle=%E4%B8%AD%E5%85%B4%E9%80%9A%E8%AE%AF&cid=4895084926073564&pageIndex=1&limit=50&sort=datetime&order=desc')
# for i in myArray:
#     print(i)
D = downloader.Downloader()
result = D('http://app.jg.eastmoney.com/Report/Search.do?securitycodes=000063.SZ&gridTitle=%E4%B8%AD%E5%85%B4%E9%80%9A%E8%AE%AF&cid=4895084926073564&pageIndex=1&limit=50&sort=datetime&order=desc')
# print(json.loads(result.decode('utf-8')).get('records'))
records = json.loads(result.decode('utf-8')).get('records')
for item in records:
    print(item)