#!/usr/bin/python3
seed = __import__('seed')

# Connect directly to the ALX_prodev database
connection = seed.connect_to_prodev()

if connection:
    print("Streaming rows one by one:\n")

    for user in seed.stream_users(connection):
        print(user)
        # stop after a few rows for testing
        if user['age'] > 100:
            break

    connection.close()

    
