#!/usr/bin/env python3
"""Task 5: Least Frequently Used (LFU) Caching System."""

from collections import OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFU cache system with item frequency tracking and eviction."""

    def __init__(self):
        """Initialize the cache and frequency tracker."""
        super().__init__()
        self.cache_data = OrderedDict()
        self.usage_counts = {}

    def __reorder_cache(self, key):
        """Update the frequency of a key and reorder cache based on frequency."""
        self.usage_counts[key] += 1
        self.cache_data.move_to_end(key, last=True)

    def put(self, key, item):
        """Add item to the cache, evicting the least frequently used if full."""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                least_used = min(self.usage_counts, key=self.usage_counts.get)
                print("DISCARD:", least_used)
                self.cache_data.pop(least_used)
                del self.usage_counts[least_used]
            self.cache_data[key] = item
            self.usage_counts[key] = 1
        else:
            self.cache_data[key] = item
            self.__reorder_cache(key)

    def get(self, key):
        """Retrieve item from cache by key, updating its usage count."""
        if key in self.cache_data:
            self.__reorder_cache(key)
        return self.cache_data.get(key, None)
