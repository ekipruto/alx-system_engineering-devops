#!/usr/bin/env python3
import sqlite3
import functools


def log_queries(func):
    """Decorator that logs the SQL query before executing it"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("No SQL query provided.")
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
