# Gets all message history for a given channel
import discord
import src.config as config


async def get_count_guild(client, count_guild_id):
    count_guild = await client.fetch_guild(count_guild_id)
    return count_guild


async def get_count_channel(count_guild, count_chan_id):
    count_channel = await count_guild.fetch_channel(count_chan_id)
    return count_channel


def get_msg_to_search_after(count_channel, search_after_msg_id):
    search_after_msg = count_channel.get_partial_message(search_after_msg_id).created_at
    return search_after_msg


async def get_count_history(count_channel, search_after):
    all_messages = []
    # Fetch all messages, starting from most recent
    async for msg in count_channel.history(limit=None,
                                           before=None,
                                           after=search_after,
                                           around=None,
                                           oldest_first=True):
        print(msg.content)
        all_messages.append(msg)
        # Check message content to see if it contains the number `1` (and only the number `1`)
        # if get_latest_start_count(msg):
        #     start_count = msg
        #     print(f'\n***Start Count: {start_count.content}\n')
        #     break
    return all_messages


def get_latest_start_count(message):
    if message.content.startswith('1 '):
        return message
    return None
