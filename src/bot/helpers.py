# Gets all message history for a given channel
import json
import pickle
import time
from datetime import timedelta
from typing import List, Any


async def get_count_guild(client, count_guild_id, **kwargs):
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Getting discord.Guild object for count_guild_id: {count_guild_id}`')
    count_guild = await client.fetch_guild(count_guild_id)
    if verbose:
        print(f'  Success! Retrieved discord guild for using client.')
    return count_guild


async def get_count_channel(count_guild, count_chan_id, **kwargs):
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Getting discord.Channel object in guild using channel id: {count_chan_id}`')
    count_channel = await count_guild.fetch_channel(count_chan_id)
    if verbose:
        print(f'  Success! Retrieved discord channel object using client.')
    return count_channel


def get_msg_datetime(count_channel, msg_id):
    """ Gets a UTC datetime object for a given message id.

    :param count_channel: a discord.channel object
    :param msg_id: the message id for which we want a datetime object
    :return: datetime of given msg_id in a discord.Channel instance
    """
    msg_dt = count_channel.get_partial_message(msg_id).created_at
    return msg_dt


def parse_channel_message(msg, **kwargs):
    message = {'msg_id': int(msg.id),
               'auth_id': int(msg.author.id),
               'content': str(msg.content),
               'created_at': msg.created_at,
               'edited_at': msg.edited_at if msg.edited_at else None,
               # 'created_at': msg.created_at.timestamp(),
               # 'edited_at': msg.edited_at.timestamp() if msg.edited_at else None,
               'reactions': str(msg.reactions),
               }
    return message


def parse_channel_messages(channel_msgs, **kwargs):
    """ Given a collection of channel messages, parse them into an appropriate format for db storage.

    :param channel_msgs: one or more channel messages from a channel to be formatted
    :return: a formatted collection of parsed channel messages.
    """
    # <Message id=1053023864046751774 channel=<TextChannel id=1038808890466390066 name='the-quest-to-10k' position=2 nsfw=False news=False category_id=780312283746009128> type=<MessageType.default: 0> author=<User id=82982763317166080 name='ahi' global_name='Ahi' bot=False> flags=<MessageFlags value=0>>
    verbose = kwargs.get('verbose')

    all_messages = []
    server_channels: list[Any] = []
    for msg in channel_msgs:
        server_channel = {'guild_name': str(msg.guild.name),
                          'guild_id': int(msg.guild.id),
                          'count_chan_name': str(msg.channel.name),
                          'count_chan_id': int(msg.channel.id),
                          'last_msg_id': int(msg.channel.last_message_id),
                          'updated_at': ''
                          }
        server_channels.extend([server_channel] if server_channel not in server_channels else [])
        message = parse_channel_message(msg, **kwargs)

        all_messages.append(message)
    return {'messages': all_messages, 'servers': server_channels}


def save_channel_msgs_to_json(channel_msgs, filename='count_history.json', folder='data/', **kwargs):
    """ Saves a collection of channel messages to a local json file.

    :param folder:
    :param channel_msgs: a collection of channel messages from the message history
    :param filename: the name of the filename where channel messages should be saved
    :param kwargs: verbose
    :return: noreturn
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Now saving {len(channel_msgs)} channel messages as:  `data/{filename}`')
    with open(folder + filename, 'w', encoding='utf-8') as fh:
        json.dump(channel_msgs, fh, ensure_ascii=False, indent=4)
    if verbose:
        print(f'  Success!  Saved {len(channel_msgs)} messages to:  `data/{filename}`')


def write_pickle_results(some_results, filename, folder='data/', **kwargs):
    """ Saves a collection of channel messages to a local json file.

    :param folder:
    :param some_results: results after using a client to fetch some messages
    :param filename: the name of the pickle file to save as, including extension
    :param kwargs: verbose
    :return:
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Saving results to: `data/{filename}`')
    with open(folder + filename, 'wb') as fh:
        pickle.dump(some_results, fh, protocol=pickle.HIGHEST_PROTOCOL)
        if verbose:
            print(f'  Success!  Saved results to: `data/{filename}`')


def load_pickle_results(filename, folder='data/', **kwargs):
    """ Loads a pickled object from a local file..

    :param folder:
    :param filename: the name of the pickle file to load from, including extension
    :param kwargs: verbose
    :return: result
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Loading results from: `data/{filename}`')
    with open(folder + filename, 'rb') as fh:
        result = pickle.load(fh)
        if verbose:
            print(f'  Success!  Loaded results from: `data/{filename}`')
    return result


async def get_count_history(count_channel, search_after, **kwargs):
    all_messages = []
    verbose = kwargs.get('verbose')
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


def get_latest_start_count(message):
    if message.content.startswith('1 '):
        return message
    return None
