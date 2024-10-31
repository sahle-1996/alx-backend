#!/usr/bin/env python3
"""Task 3: Deletion-resilient hypermedia pagination."""

import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate start and end indexes for given page and size."""
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a dataset of baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Loads or retrieves the dataset from the CSV file."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                self.__dataset = [row for row in reader][1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Returns the dataset indexed by original row number."""
        return {i: row for i, row in enumerate(self.dataset())}

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns a page of dataset rows."""
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        return self.dataset()[start:end]

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Returns paginated data that handles dynamic deletions."""
        data = self.indexed_dataset()
        assert isinstance(index, int) and 0 <= index < len(data)
        
        paginated_data = []
        next_index, current_size = index, 0
        
        while current_size < page_size and next_index < len(data):
            if next_index in data:
                paginated_data.append(data[next_index])
                current_size += 1
            next_index += 1
        
        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(paginated_data),
            'data': paginated_data
        }
