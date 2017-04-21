import urllib.parse
import urllib.request
import random
import time
from datetime import datetime, timedelta
import socket
import json

DEFAULT_AGENT = 'wl'
DEFAULT_DELAY = 60
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        print('__call__')
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # 缓存中没有
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    #
                    result = None
        if result is None:
            # 没有缓存 需要下载
            print('down_before')
            self.throttle.wait(url)
            print('down_affert')
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                # 缓存起来
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print
        'Downloading:', url
        request = urllib.request.Request(url, data, headers or {})
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print
            'Download error:', str(e)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # 500错误 从新尝试请求
                    return self._get(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}


class Throttle:
    """对同一个域名的访问的限速
    """

    def __init__(self, delay):
        # 同一个域名的多个请求之间的延时时间
        self.delay = delay
        # 一个域名的最后访问的时间戳
        self.domains = {}

    def wait(self, url):
        """如果最近访问过这个域名 就延时
        """
        domain = urllib.parse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()
