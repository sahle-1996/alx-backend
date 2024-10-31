#!/usr/bin/env python3
"""Task 1: Pagination system implementation."""

import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate start and end index for the given pagination parameters."""
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a dataset of popular baby names."""
    
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__records = None

    def dataset(self) -> List[List]:
        """Returns cached dataset or loads it from the CSV file if not loaded."""
        if self.__records is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                self.__records = [row for row in reader][1:]
        return self.__records

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns a specific page of records from the dataset."""
        assert isinstance(page, int) and isinstance(page_size, int), "Arguments must be integers"
        assert page > 0 and page_size > 0, "Arguments must be positive"
        
        start_idx, end_idx = index_range(page, page_size)
        data = self.dataset()
        
        if start_idx >= len(data):
            return []
        return data[start_idx:end_idx]
