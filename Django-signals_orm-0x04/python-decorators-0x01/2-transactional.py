import sqlite3
import functools

def with_db_connection(func):
    """A decorator to handle opening and closing database connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn=sqlite3.connect("users.db")
        try:
            result=func(conn, *args,**kwargs)
            return result
        finally:
            conn.close()

    return wrapper
import functools

def transactional(func):
    """A decorator to manage database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper
    return wrapper
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update a user's email address."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))