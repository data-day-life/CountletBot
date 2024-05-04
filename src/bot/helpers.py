# /src/bot/helpers.py

import json
import pickle
from datetime import datetime


def get_msg_datetime(count_channel, msg_id):
    """ Gets a UTC datetime object for a given message id.

    :param count_channel: a discord.channel object
    :type count_channel: a discord.TextChannel
    :param msg_id: the message id for which we want a datetime object
    :type msg_id: str or int
    :return: datetime of given msg_id in a discord.Channel instance
    """
    msg_dt = count_channel.get_partial_message(msg_id).created_at
    return msg_dt


def parse_channel_message(msg):
    """ Given a single message, parse out the relevant fields and return a dictionary.

    :param msg: a single message from a discord channel
    :type msg: a discord.Message
    :return: a dictionary of parsed message fields
    :rtype: dict
    """
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
    :type channel_msgs: discord.TextChannel.history
    :param kwargs: verbose
    :type kwargs: dict
    :return: a formatted collection of parsed channel messages.
    """

    # <Message id=1053023864046751774 channel=<TextChannel id=1038808890466390066 name='the-quest-to-10k' position=2
    # nsfw=False news=False category_id=780312283746009128> type=<MessageType.default: 0> author=<User
    # id=82982763317166080 name='ahi' global_name='Ahi' bot=False> flags=<MessageFlags value=0>>
    server_channel = dict()
    # def get_channel_info(msg):
    #     server_channel = {'guild':
    #                           {'guild_name': str(msg.guild.name),
    #                            'guild_id': int(msg.guild.id),
    #                            'count_chan_name': str(msg.channel.name),
    #                            'count_chan_id': int(msg.channel.id),
    #                            'last_msg_id': int(msg.channel.last_message_id),
    #                            'messages': []
    #                            }
    #                       }
    #     return server_channel
    if kwargs.get('verbose'):
        print(f'Parsing {len(channel_msgs)} channel messages...')
    for msg in channel_msgs:
        parsed_message = parse_channel_message(msg)
        channel_messages = server_channel[int(msg.guild.id)].get('messages', [])
        channel_messages.append(parsed_message)
        all_messages = {'guild_name': str(msg.guild.name),
                        'count_chan_name': str(msg.channel.name),
                        'count_chan_id': int(msg.channel.id),
                        'last_msg_id': int(msg.channel.last_message_id),
                        'messages': channel_messages,
                        }
        server_channel.update({int(msg.guild.id): all_messages})
    return server_channel


def save_channel_msgs_to_json(channel_msgs, filename='count_history.json', folder='data/', **kwargs):
    """ Saves a collection of channel messages to a local json file.

    :param channel_msgs: a collection of parsed channel messages from the message history
    :type channel_msgs: dict
    :param filename: the name of the filename to write channel messages to disk
    :type filename: string
    :param folder: the name of the folder in which to store the .json file
    :type folder: string
    :param kwargs: verbose
    :type kwargs: dict
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
    """ Saves a collection of channel messages to a local pickle file.

    :param some_results: a collection of parsed channel messages from the message history
    :type some_results: dict
    :param filename: the name of the filename to write channel messages to disk
    :type filename: string
    :param folder: the name of the folder in which to store the .pk file
    :type folder: string
    :param kwargs: verbose
    :type kwargs: dict
    :return: noreturn
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Saving results to: `data/{filename}`')
    with open(folder + filename, 'wb') as fh:
        pickle.dump(some_results, fh, protocol=pickle.HIGHEST_PROTOCOL)
        if verbose:
            print(f'  Success!  Saved results to: `data/{filename}`')


def load_pickle_results(filename, folder='../data/', **kwargs):
    """ Loads a pickled object from a local file.

    :param filename: the name of the filename to read channel messages from disk
    :type filename: string
    :param folder: the name of the folder in which to fetch the .pk file
    :type folder: string
    :param kwargs: verbose
    :type kwargs: dict
    :return: dictionary of channel messages
    """
    verbose = kwargs.get('verbose')
    if verbose:
        print(f'Loading results from: `{folder}{filename}`')
    with open(folder + filename, 'rb') as fh:
        result = pickle.load(fh)
        if verbose:
            print(f'  Success!  Loaded results from: `data/{filename}`')
    return result


def get_timestamp_string():
    """ Returns a formatted timestamp string for the current time; a helper for uniquely naming save_files.

    :return: a string of 'YYYY-mm-dd__hh-mm-ss' for the current time
    :rtype: str
    """
    now = datetime.now()
    formatted_timestamp = now.strftime('%Y-%m-%d__%H-%M-%S')
    return formatted_timestamp


def main(**kwargs):
    pass


if __name__ == '__main__':
    main()
