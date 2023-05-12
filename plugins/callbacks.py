import os
import logging
import asyncio
import tmdbsimple as tmdb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Callback query handler
@Client.on_callback_query("get_details")
async def callback_query(client, callback_query):
    tmdb_id = callback_query.data.split(":")[1]
    details = tmdb.Movies(tmdb_id).info() if "movie" in tmdb.Movies(tmdb_id).info() else tmdb.TV(tmdb_id).info()
    text = f"<b>{details['title']}</b>\n" if "title" in details else f"<b>{details['name']}</b>\n"
    text += f"Release date: {details['release_date']}\n" if "release_date" in details else ""
    text += f"First air date: {details['first_air_date']}\n" if "first_air_date" in details else ""
    text += f"Overview: {details['overview']}"
    await callback_query.message.edit_text(
        text,
        parse_mode="html",
    )
