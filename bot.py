import os
import logging
import pyrogram

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    app = pyrogram.Client(
        "tmdb bot",
        bot_token='1958907987:AAGql9FNP28u8ZhR5ZlFFkmzuKbIbWKDIyQ',
        api_id='950903',
        api_hash='69d37ae7fdf5154293b01434044c37dd',
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
