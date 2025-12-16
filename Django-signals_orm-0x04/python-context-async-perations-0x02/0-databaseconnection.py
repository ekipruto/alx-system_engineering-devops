#!/usr/bin/python3
import sqlite3


class DatabaseConnection:
    """Custom context manager for handling SQLite database connections."""

    def __init__(self, db_name):
        """Initialize with database name."""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open database connection when entering the context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close database connection when exiting the context."""
        if self.conn:
            self.conn.close()
        # Returning False will propagate exceptions if they occur
        return False


# Using the context manager to fetch users
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
