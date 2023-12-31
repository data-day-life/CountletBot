import asyncio
import logging
import logging.handlers
from typing import List, Optional
import asyncpg
import discord
from discord.ext import commands
from aiohttp import ClientSession

import config as cfg
import helpers


class CustomBot(commands.Bot):
    def __init__(self,
                 *args,
                 initial_extensions: List[str],
                 db_pool: asyncpg.Pool,
                 web_client: ClientSession,
                 testing_guild_id: Optional[int] = None,
                 testing_chan_id: Optional[int] = None,
                 **kwargs,
                 ):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.testing_chan_id = testing_chan_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # Here, we are loading extensions prior to sync.
        # This ensures we are syncing interactions defined in those extensions.
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)
        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.
        # Use the db_pool for database operations
        async with self.db_pool.acquire() as connection:
            # Use the connection for executing queries
            await connection.execute('SELECT * FROM my_table')


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


async def main():
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
            await bot.start(cfg.CLIENT_TOKEN)
            results = await helpers.cold_boot(our_client, verbose=True)


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(main())
