#!/usr/bin/python3
import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',   # update if you set a MySQL root password
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
