#!/usr/bin/env python3
"""Task 2: Hypermedia pagination with additional metadata."""

import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate start and end index based on pagination parameters."""
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return start_idx, end_idx


class Server:
    """Server class to paginate a dataset of popular baby names."""
    
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__records = None

    def dataset(self) -> List[List]:
        """Loads or retrieves the cached dataset from the CSV file."""
        if self.__records is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                self.__records = [row for row in reader][1:]
        return self.__records

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns a page of dataset records."""
        assert isinstance(page, int) and isinstance(page_size, int), "Args must be integers"
        assert page > 0 and page_size > 0, "Args must be positive"
        
        start_idx, end_idx = index_range(page, page_size)
        data = self.dataset()
        
        if start_idx >= len(data):
            return []
        return data[start_idx:end_idx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Returns a dictionary of pagination data and metadata."""
        page_data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        
        return {
            'page_size': len(page_data),
            'page': page,
            'data': page_data,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': total_pages
        }
