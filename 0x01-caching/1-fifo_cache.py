#!/usr/bin/env python3

'''Task 1: First-In, First-Out (FIFO) Caching System'''

from collections import OrderedDict
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    '''FIFO caching system that inherits from BaseCaching.'''

    def __init__(self):
        '''Initialize the cache with an ordered dictionary.'''
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        '''Add `item` to the cache with `key`. Remove oldest if full.'''
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            oldest_key, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {oldest_key}")

        self.cache_data[key] = item

    def get(self, key):
        '''Retrieve value from cache by `key`.'''
        return self.cache_data.get(key)
