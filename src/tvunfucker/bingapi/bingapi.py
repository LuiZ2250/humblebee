#!/usr/bin/env/python
#encoding:utf-8

"""
Simple json interface to the bing search api, with caching.
"""
import base64
from urllib2 import (build_opener, 
Request, HTTPSHandler, 
HTTPBasicAuthHandler, 
HTTPPasswordMgrWithDefaultRealm,
Request)
from urllib import quote, urlencode
import os
from tempfile import gettempdir
import logging

from tvdb_cache import CacheHandler

#temporary, don't keep it here
API_KEY = '3cgOZAjtF9AGYtQedrKJlIC8p0Q8ScM2eOHGfZ4zT6A='

TOP_LEVEL_URL = '''
https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web
'''
SEARCH_URL = '''
https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query=%%27%(qstring)s%%27&$top=50&$format=json
'''

log = logging.getLogger('bingapi')

class Bing(object):
    def __init__(self, api_key=None, caching=True):
        self.api_key = api_key
        self.caching = caching
        self.cache_dir = os.path.join(
            gettempdir(), 'bing'
            )

        self.url_opener = self.get_opener()

    def get_opener(self):
        """
        pwmgr = HTTPPasswordMgrWithDefaultRealm()
        pwmgr.add_password(
            None,
            url,
            self.api_key,
            self.api_key
            )
        authhandler = HTTPBasicAuthHandler(pwmgr)        
        """
        
        if self.caching:
            log.debug('There is fucking caching')
            return build_opener(
                CacheHandler(self.cache_dir)
        #authhandler
                )
        return build_opener(
        #authhandler
            )

    def search(self, query, recache=False):
        url = SEARCH_URL % {'qstring' : quote(query.encode('utf-8'))}
        req = Request(url)
        bsixfour = base64.encodestring(
            '%s:%s' % (self.api_key, self.api_key)
            ).replace('\n', '')
        req.add_header('Authorization', 'Basic %s' % bsixfour)
        
        opener = self.url_opener        
        log.debug('opening url: %s', url)
        response = opener.open(req)
        if 'x-local-cache' in response.headers:
            log.debug(
                'URL \'%s\' was cached in \'%s\'', 
                url, 
                response.headers['x-local-cache']
                )
            if recache:
                log.debug('attempting to recache url: %s', url)
                response.recache()
        return response.read()            
                               

class Result(object):
    pass


def main():
    turl = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query=%27what%27&$top=50&$format=json'
    hndlr = logging.StreamHandler()
    frmtr = logging.Formatter(
        '%(levelname)s:%(module)s.%(funcName)s: %(message)s'
        )
    hndlr.setFormatter(frmtr)
    log.addHandler(hndlr)
    log.setLevel(logging.DEBUG)
    b = Bing(api_key=API_KEY, caching=True)
    b.search('cake fart')
    b.search('cake fart')

if __name__ == '__main__':
    main()
    
