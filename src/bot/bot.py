# /src/bot/bot.py
import time
from datetime import timedelta

import config as cfg
import src.config as cfg
import discord
import helpers
from bot.helpers import get_msg_datetime, parse_channel_messages, \
    get_timestamp_string, save_channel_msgs_to_json, write_pickle_results

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

    await cold_boot(client)
    pass


client.run(cfg.CLIENT_TOKEN)


async def cold_boot(discord_client, **kwargs):
    """ Connects to a guild and counting channel, collects the message history and saves it.

    :param discord_client: a discord.Client object
    :return: the collected messages from a discord server's counting channel.
    """
    count_guild = await get_count_guild(discord_client, cfg.GUILD_ID, **kwargs)
    count_channel = await get_count_channel(count_guild, cfg.COUNT_CHAN_ID, **kwargs)
    search_after = get_msg_datetime(count_channel, cfg.SEARCH_AFTER_MSG_ID)
    # Fetch and parse messages.
    messages = await get_count_history(count_channel, search_after, **kwargs)
    parsed_msgs = parse_channel_messages(messages, **kwargs)
    # Save the messages to a file.
    f_name = f'cold_boot_count_history--{get_timestamp_string()}'
    save_channel_msgs_to_json(channel_msgs=parsed_msgs, filename=f'{f_name}.json', **kwargs)
    write_pickle_results(parsed_msgs, filename=f'{f_name}.pk', **kwargs)
    return parsed_msgs


async def get_count_guild(discord_client, count_guild_id, **kwargs):
    """ Given a discord client, connect to a guild ("discord server") using a guild id.

    :param discord_client: a valid Discord client
    :type discord_client: discord.Client
    :param count_guild_id: a numeric id for the discord counting server
    :type count_guild_id: str or int
    :param kwargs: verbose
    :type kwargs: dict
    :return: a discord.Guild object for the given count_guild_id
    :rtype: discord.Guild
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Getting discord.Guild object for count_guild_id: {count_guild_id}`')
    count_guild = await discord_client.fetch_guild(count_guild_id)
    if verbose:
        print(f'  Success! Retrieved discord guild for using client.')
    return count_guild


async def get_count_channel(count_guild, count_chan_id, **kwargs):
    """ Given a discord server connection, connect to the counting channel using a channel id.

    :param count_guild: a discord.Guild object
    :type count_guild: discord.Guild
    :param count_chan_id: a numeric id for the discord counting channel
    :type count_chan_id: str or int
    :param kwargs: verbose
    :type kwargs: dict
    :return: the counting channel for the given discord server (count_guild).
    :rtype: discord.Channel
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Getting discord.Channel object in guild using channel id: {count_chan_id}`')
    count_channel = await count_guild.fetch_channel(count_chan_id)
    if verbose:
        print(f'  Success! Retrieved discord channel object using client.')
    return count_channel


async def get_count_history(count_channel, search_after, **kwargs):
    """ Given a discord channel, fetch all message history for that channel for search_after.

    :param count_channel: a discord channel which contains counting history
    :type count_channel: discord.Channel
    :param search_after: a message_id after which the history should be collected (exclusive)
    :type search_after: str or int
    :param kwargs: verbose
    :type kwargs: dict
    :return: a list of all messages that comprise count_history
    :rtype: list
    """
    all_messages = []
    verbose = kwargs.get('verbose')
    start = time.time()
    if verbose:
        print('Fetching count history from count channel...')
        start = time.time()
    # Fetch all messages
    async for msg in count_channel.history(limit=250,
                                           before=None,
                                           after=search_after,
                                           around=None,
                                           oldest_first=True):
        all_messages.append(msg)
    if verbose:
        print(f'  Success!  Fetched {len(all_messages)} messages from counting channel.')
        print(f'    took {str(timedelta(seconds=(time.time() - start)))} sec.')
    return all_messages
