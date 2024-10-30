#!/usr/bin/env python3
"""Task 3: Least Recently Used (LRU) Caching System"""

from collections import OrderedDict
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU caching system that inherits from BaseCaching."""

    def __init__(self):
        """Initialize the cache with an ordered dictionary."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache and remove the least recently used if full."""
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key, _ = self.cache_data.popitem(last=False)
            print(f"DISCARD: {lru_key}")

        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=False)

    def get(self, key):
        """Retrieve an item from the cache by key and mark it as recently used."""
        if key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key)
