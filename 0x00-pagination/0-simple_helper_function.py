#!/usr/bin/env python3
"""Helper function for pagination.
"""
from typing import Tuple


def get_index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculates the start and end index for a pagination page.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index
