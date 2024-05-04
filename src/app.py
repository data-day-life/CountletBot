# /src/app.py
from bot import helpers


def main(**kwargs):
    helpers.main(verbose=True, **kwargs)


if __name__ == '__main__':
    main()  # This is the entry point for the bot process.
