#!/usr/bin/env python3
"""Task 2: Last-In, First-Out (LIFO) Caching System"""

from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Cache system implementing LIFO (Last-In, First-Out) eviction."""

    def __init__(self):
        """Initialize the cache with an ordered dictionary."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache and remove the most recent if full."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
            last_key, _ = self.cache_data.popitem(last=True)
            print(f"DISCARD: {last_key}")

        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """Retrieve an item from the cache by key."""
        return self.cache_data.get(key)
