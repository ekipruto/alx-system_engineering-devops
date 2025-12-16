#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import uuid

# --- Connect to MySQL server ---
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="root"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# --- Create database if not exists ---
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()


# --- Connect directly to ALX_prodev database ---
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# --- Create user_data table ---
def create_table(connection):
    cursor = connection.cursor()
    table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    );
    """
    cursor.execute(table_query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


# --- Insert CSV data ---
def insert_data(connection, csv_path):
    df = pd.read_csv(csv_path)

    cursor = connection.cursor()
    for _, row in df.iterrows():
        user_id = str(uuid.uuid4())
        name = row['name']
        email = row['email']
        age = int(row['age'])
        cursor.execute(
            "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
            (user_id, name, email, age)
        )
    connection.commit()
    cursor.close()
    print(f"Inserted {len(df)} rows into user_data table")

    # --- Generator function to stream rows one by one ---
def stream_users(connection):
    """
    A generator that yields one row at a time from the user_data table.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row  # return one record at a time

        cursor.close()
    except Exception as e:
        print(f"Error streaming users: {e}")

