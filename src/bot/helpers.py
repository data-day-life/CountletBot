# Gets all message history for a given channel

starting_count_msg_id = 1050903420439101471

async def get_count_history(channel, search_after):
    all_messages = []
    start_count = None
    # Fetch all messages, starting from most recent
    async for msg in channel.history(limit=None,
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


