import os
import asyncio
import tmdbsimple as tmdb
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Start command
@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Hello! I am the TMDB Bot. You can use me to search for information about movies and TV shows. Just type /help to get started!"
    )

# Help command
@Client.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = "To search for a movie or TV show, simply type /search followed by the name of the movie or show. For example, /search The Matrix."
    await message.reply_text(help_text)

# Search command
@Client.on_message(filters.command("search"))
async def search_command(client, message):
    # Get query from message
    query = " ".join(message.command[1:])
    
    # Search for movies and TV shows
    search = tmdb.Search()
    search.multi(query)
    
    # Check if any results were found
    if len(search.results) == 0:
        await message.reply_text("Sorry, no results were found for that query.")
        return
    
    # Create inline keyboard with search results
    keyboard = []
    for result in search.results:
        title = result["title"] if "title" in result else result["name"]
        keyboard.append([InlineKeyboardButton(title, callback_data=f"details:{result['id']}")])
    
    # Send message with inline keyboard
    await message.reply_text(
        "Here are the search results:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
