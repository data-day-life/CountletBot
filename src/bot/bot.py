import os
import random
import discord
import helpers

token = os.getenv("CLIENT_TOKEN")
count_guild_id = os.getenv("GUILD_ID")
count_chan_id = os.getenv('COUNT_CHAN_ID')
# my_guild = 780312283233779713
guild_name = 'Kaiyacord'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # Now that the bot is connected, do something
    count_guild = await client.fetch_guild(count_guild_id)
    count_channel = await count_guild.fetch_channel(count_chan_id)

    starting_count_msg_id = 1053012296370229248
    search_after = count_channel.get_partial_message(starting_count_msg_id).created_at
    print('Fetching count history from count channel')
    messages = await helpers.get_count_history(count_channel, search_after)

    pass

client.run(token)
