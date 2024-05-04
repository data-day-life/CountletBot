# /src/app.py
from bot import helpers

"""
Create a connection to a sqlite database running in a docker container.  
Also create a discord client and connect to the appropriate guild and channel to collect count_history.

If the most recently received message in the sqlite database does not match the most recently received message 
according to the discord client, update the database according to the message history collected by the discord 
client.  
Otherwise, maintain a connection to the database to update tables as new messages arrive from the discord client.  
"""


def main(**kwargs):
    helpers.main(verbose=True, **kwargs)


if __name__ == '__main__':
    main()  # This is the entry point for the bot process.
