from typing import List, Optional
import asyncpg
import discord
from discord.ext import commands
from aiohttp import ClientSession


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
        # We can also use the web client to make requests to external services.
        async with self.web_client.get('https://httpbin.org/get') as resp:
            # Use resp to get the data from the response
            pass
