#!/usr/bin/python3
import sqlite3
import functools
import time


# Global cache dictionary
query_cache = {}


def with_db_connection(func):
    """Decorator to handle opening and closing the database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """Decorator that caches database query results based on SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Retrieve the query string from arguments or kwargs
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None

        # Check if query result is already cached
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]

        # If not cached, execute and store in cache
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        print("Caching result for query:", query)
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users and cache results to avoid redundant DB calls."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
