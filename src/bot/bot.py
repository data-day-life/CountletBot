import discord
import helpers
import src.config as config

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # Now that the bot is connected, do something
    count_guild = helpers.get_count_guild(client, config.GUILD_ID)
    count_channel = helpers.get_count_channel(count_guild, config.COUNT_CHAN_ID)

    print('Fetching count history from count channel...')
    search_after = helpers.get_msg_to_search_after(count_channel, config.SEARCH_AFTER_MSG_ID)
    messages = await helpers.get_count_history(count_channel, search_after)

    pass


client.run(token)
