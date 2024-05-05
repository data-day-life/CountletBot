# /src/app.py
import os
import asyncio
import asyncpg
import logging
import logging.handlers
from aiohttp import ClientSession
import discord
from discord.ext import commands

from bot.adv_bot import CustomBot

from bot import helpers
"""
Create a connection to a sqlite database running in a docker container.  
Also create a discord client and connect to the appropriate guild and channel to collect count_history.

If the most recently received message in the sqlite database does not match the most recently received message 
according to the discord client, update the database according to the message history collected by the discord 
client.  
Otherwise, maintain a connection to the database to update tables as new messages arrive from the discord client.  
"""
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
CLIENT_TOKEN = os.environ.get('CLIENT_TOKEN', None)


def setup_logging():
    # 1. logging

    # for this example, we're going to set up a rotating file logger.
    # for more info on setting up logging,
    # see https://discordpy.readthedocs.io/en/latest/logging.html and https://docs.python.org/3/howto/logging.html

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


async def connect_to_database():
    pool = await asyncpg.create_pool(
        host='localhost',
        port=5432,
        user='your_username',
        password='your_password',
        database='your_database',
    )
    try:
        yield pool
    finally:
        await pool.close()


async def get_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)


def get_discord_client():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    return client


async def main(**kwargs):
    # discord_bot = get_discord_client()
    # discord_bot.run(CLIENT_TOKEN)
    #
    # db_pool = get_db_pool()
    # db_conn = db_pool.acquire()
    # db_conn.close()
    # db_pool.close()
    # db_pool.terminate()
    # return
    # When taking over how the bot process is run, you become responsible for a few additional things.
    logger = setup_logging()

    # Here we have a web client and a database pool, both of which do cleanup at exit.
    # We also have our bot, which depends on both of these.
    async with (ClientSession() as our_client, connect_to_database() as db_pool):
        # 2. We become responsible for starting the bot.
        exts = ['general', 'dice']
        exts = []
        intents = discord.Intents.default()
        intents.message_content = True
        async with CustomBot(commands.when_mentioned,
                             db_pool=db_pool,
                             web_client=our_client,
                             initial_extensions=exts,
                             intents=intents,
                             ) as bot:
            await bot.start(CLIENT_TOKEN)
            # results = await bot.cold_boot(our_client, verbose=True)


if __name__ == '__main__':
    # For most use cases, after defining what needs to run, we can just tell asyncio to run it:
    asyncio.run(main())  # This is the entry point for the bot process.
