import src.config as cfg
import discord
import helpers

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    # Now that the bot is connected, do something
    # count_guild = await helpers.get_count_guild(client, cfg.GUILD_ID)
    # count_channel = await helpers.get_count_channel(count_guild, cfg.COUNT_CHAN_ID)
    #
    # search_after = helpers.get_msg_datetime(count_channel, cfg.SEARCH_AFTER_MSG_ID)
    # messages = await helpers.get_count_history(count_channel, search_after, verbose=True)
    # count_history = helpers.parse_channel_messages(messages, **kwargs)
    # f_name = 'count_history'
    # helpers.write_pickle_results(count_history, filename=f_name, verbose=True)

    await helpers.cold_boot(client)
    pass


client.run(cfg.CLIENT_TOKEN)
