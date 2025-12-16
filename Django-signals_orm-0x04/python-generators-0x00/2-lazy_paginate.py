#!/usr/bin/python3
"""
2-lazy_paginate.py

Provides:
- paginate_users(page_size, offset): fetches a page from user_data
- lazy_pagination(page_size): generator that lazily fetches pages starting at offset 0
"""

from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """
    Fetch a single page of rows starting at offset.
    Returns a list of dictionaries (rows) or an empty list if none.
    """
    connection = connect_to_prodev()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    # Use parameterized query to avoid SQL injection and formatting issues
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that yields pages (lists of rows) one by one.
    Starts at offset 0 and increments by page_size.
    Uses exactly one loop.
    """
    offset = 0
    while True:                       # single loop required by the task
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Backwards-compatible alias (in case test expects lazy_paginate)
lazy_paginate = lazy_pagination
