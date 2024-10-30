#!/usr/bin/env python3
"""Task 4: Most Recently Used (MRU) Caching System."""

from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU cache system implementing the BaseCaching system."""

    def __init__(self):
        """Initialize the cache as an ordered dictionary."""
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Store an item in the cache, evicting the most recent if full."""
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key, _ = self.cache_data.popitem(last=True)
            print(f"DISCARD: {mru_key}")

        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """Retrieve an item by key and mark it as most recently used."""
        if key in self.cache_data:
            self.cache_data.move_to_end(key, last=True)
        return self.cache_data.get(key)
