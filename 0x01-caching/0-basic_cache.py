#!/usr/bin/env python3

'''A simple caching system.'''

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    '''Simple cache implementation that inherits from BaseCaching.'''

    def put(self, key, item):
        '''Store `item` in cache with the specified `key`.'''
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        '''Retrieve the cache value associated with `key`.'''
        return self.cache_data.get(key)
