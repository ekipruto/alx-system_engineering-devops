#!/usr/bin/python3
import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously from the database."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results


async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            return results


async def fetch_concurrently():
    """Run both async queries concurrently."""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", results_all)
    print("Users older than 40:", results_older)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
