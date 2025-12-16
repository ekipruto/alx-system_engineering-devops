# Python Generators — ALX Backend

## Objective
Create a generator that streams rows from a MySQL database one by one.

## Setup
1. Create the database and table with `0-main.py`
2. Stream rows using the generator in `1-main.py`

## Functions
- `connect_db()` — connects to MySQL
- `create_database()` — creates ALX_prodev
- `connect_to_prodev()` — connects to the database
- `create_table()` — creates user_data table
- `insert_data()` — seeds table from CSV
- `stream_users()` — generator streaming rows one by one
