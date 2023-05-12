import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Set up Pyrogram client
api_id = int(environ['API_ID'])
api_hash = environ['API_HASH']
bot_token = environ['BOT_TOKEN']


# Set up TMDB API key
tmdb.API_KEY = os.environ.get("TMDB_API_KEY")
