#!/usr/bin/env python3
"""Least Recently Used (LRU) caching implementation."""

from collections import OrderedDict
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU caching system using BaseCaching as a base class."""

    def __init__(self):
        """Set up the cache as an ordered dictionary."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Store an item in the cache and apply LRU eviction if necessary."""
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            oldest_key, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {oldest_key}")

        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=False)

    def get(self, key):
        """Fetch an item from the cache by key, marking it as recently used."""
        if key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key)
