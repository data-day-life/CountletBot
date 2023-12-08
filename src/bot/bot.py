import src.config as cfg
import discord
import helpers
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def cold_boot(client, **kwargs):
    """ Connects to a guild and counting channel, collects the message history and saves it.

    :param client: a discord.Client object
    :return: the collected messages from a discord server's counting channel.
    """
    count_guild = await helpers.get_count_guild(client, cfg.GUILD_ID, **kwargs)
    count_channel = await helpers.get_count_channel(count_guild, cfg.COUNT_CHAN_ID, **kwargs)
    search_after = helpers.get_msg_datetime(count_channel, cfg.SEARCH_AFTER_MSG_ID)

    messages = await helpers.get_count_history(count_channel, search_after, **kwargs)
    parsed_msgs = helpers.parse_channel_messages(messages, **kwargs)

    result = {'count_guild': count_guild,
              'count_channel': count_channel,
              'search_after': search_after,
              'messages': messages,
              'parsed_msgs': parsed_msgs,
              }
    # Save the messages to a file.
    helpers.write_pickle_results(parsed_msgs['messages'], 'cold_boot_count_history.pk', **kwargs)
    # helpers.save_channel_msgs_to_json(parsed_msgs['messages'], filename='cold_boot_count_history.json', **kwargs)
    return result


@client.event
async def on_ready():
    # Now that the bot is connected, do something
    count_guild = helpers.get_count_guild(client, cfg.GUILD_ID)
    count_channel = helpers.get_count_channel(count_guild, cfg.COUNT_CHAN_ID)

    print('Fetching count history from count channel...')
    search_after = helpers.get_msg_to_search_after(count_channel, cfg.SEARCH_AFTER_MSG_ID)
    messages = await helpers.get_count_history(count_channel, search_after)

    pass


client.run(cfg.CLIENT_TOKEN)
