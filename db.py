import asyncpg
import os 

async def connect():
    connection = await asyncpg.connect(
        database=os.environ.get("DATABASE"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        host=os.environ.get("HOST"),
        port=os.environ.get("PORT")
    )
    return connection

