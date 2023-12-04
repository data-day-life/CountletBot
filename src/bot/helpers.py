# Gets all message history for a given channel
async def get_msg_history(channel):
    all_messages = []
    async for msg in channel.history(limit=100,
                                     before=None,
                                     after=None,
                                     around=None,
                                     oldest_first=None):
        all_messages.append(msg)
    return all_messages

