import os
import random
import discord

token = os.getenv("CLIENT_TOKEN")
# my_guild = os.getenv("GUILD_ID")
# my_guild = 780312283233779713
guild_name = 'Kaiyacord'
count_chan = os.getenv('COUNT_CHAN_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == guild_name:
            print(
                f"{client.user} is connected to the following guild:\n"
                f"{guild.name}(id: {guild.id})"
            )

client.run(token)