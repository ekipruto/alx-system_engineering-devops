#!/usr/bin/python3
"""
4-stream_ages.py
Memory-efficient aggregation using Python generators.
"""

from seed import connect_to_prodev


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = connect_to_prodev()
    if connection is None:
        return

    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    # Single loop yielding ages one by one
    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the generator to calculate average age of all users
    without loading the entire dataset into memory.
    """
    total_age = 0
    count = 0

    # One loop only — iterate through generator directly
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
