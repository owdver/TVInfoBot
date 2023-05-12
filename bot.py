import os
import logging
import pyrogram

logging.basicConfig(level=logging.INFO)

from config import API_ID, API_HASH, BOT_TOKEN


if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    app = pyrogram.Client(
        "tmdb_bot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        workers=300
    )
    try:
        app.start()
        app.run()
    except KeyboardInterrupt:
        app.stop()
    except Exception as e:
        logging.error(f"Error: {e}")
        app.stop()
