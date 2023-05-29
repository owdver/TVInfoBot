import requests
import telebot
from datetime import datetime
import pymongo
from pymongo import MongoClient

# Create a bot object with the token
bot = telebot.TeleBot("6230370760:AAH_5KOR3n6W93Mu-q9CEakMsOTd7Z-u5Z4")

# Connect to the MongoDB database
client = MongoClient("mongodb+srv://owdver:owdver@cluster0.pzapysa.mongodb.net/?retryWrites=true&w=majority")
db = client["tvshows"]
subscriptions = db["subscriptions"]

# Define some helper functions

def get_show_info(show_id):
    # Get the show information from the TVmaze API
    url = f"https://api.tvmaze.com/shows/{show_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_show_schedule(show_id):
    # Get the show schedule from the TVmaze API
    url = f"https://api.tvmaze.com/shows/{show_id}/episodes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_next_episode(show_id):
    # Get the next episode of the show from the schedule
    schedule = get_show_schedule(show_id)
    if schedule:
        today = datetime.today().date()
        for episode in schedule:
            airdate = datetime.strptime(episode["airdate"], "%Y-%m-%d").date()
            if airdate >= today:
                return episode
        return None
    else:
        return None

def format_show_info(show):
    # Format the show information as a message
    name = show["name"]
    genres = ", ".join(show["genres"])
    status = show["status"]
    rating = show["rating"]["average"]
    summary = show["summary"]
    message = f"<b>{name}</b>\n"
    message += f"Genres: {genres}\n"
    message += f"Status: {status}\n"
    message += f"Rating: {rating}\n\n"
    message += f"{summary}"
    return message

def format_episode_info(episode):
    # Format the episode information as a message
    name = episode["name"]
    season = episode["season"]
    number = episode["number"]
    airdate = episode["airdate"]
    airtime = episode["airtime"]
    summary = episode["summary"]
    message = f"<b>{name}</b>\n"
    message += f"Season {season}, Episode {number}\n"
    message += f"Air date: {airdate}\n"
    message += f"Air time: {airtime}\n\n"
    message += f"{summary}"
    return message

def subscribe(user_id, show_id):
    # Subscribe the user to the show in the database
    subscription = {"user_id": user_id, "show_id": show_id}
    subscriptions.update_one(subscription, {"$set": subscription}, upsert=True)

def unsubscribe(user_id, show_id):
    # Unsubscribe the user from the show in the database
    subscription = {"user_id": user_id, "show_id": show_id}
    subscriptions.delete_one(subscription)

def get_subscriptions(user_id):
    # Get the list of shows that the user is subscribed to from the database
    cursor = subscriptions.find({"user_id": user_id})
    show_ids = [subscription["show_id"] for subscription in cursor]
    return show_ids

# Define some handlers for bot commands

@bot.message_handler(commands=["start"])
def start(message):
  # Greet the user and explain how to use the bot
  user_name = message.from_user.first_name
  bot.send_message(message.chat.id, f"Hello, {user_name}! I am a TV show tracker bot. I can help you find information about your favorite shows and notify you when new episodes are airing. To use me, you can send me one of these commands:\n\n/search [show name] - to search for a show by name\n/subscribe [show id] - to subscribe to a show by its id\n/unsubscribe [show id] - to unsubscribe from a show by its id\n/subscriptions - to see your current subscriptions\n/next [show id] - to see the next episode of a show by its id\n/help - to see this message again")

@bot.message_handler(commands=["search"])
def search(message):
  # Search for a show by name using the TVmaze API
  query = message.text.split(maxsplit=1)[-1]
  url = f"https://api.tvmaze.com/search/shows?q={query}"
  response = requests.get(url)
  if response.status_code == 200:
      data = response.json()
      if data:
          # Send the first 10 results as messages
          for result in data[:10]:
              show = result["show"]
              show_id = show["id"]
              message = format_show_info(show)
              message += f"\n\nTo subscribe to this show, send /subscribe {show_id}"
              bot.send_message(message.chat.id, message, parse_mode="HTML")
      else:
          # No results found
          bot.send_message(message.chat.id, "Sorry, I could not find any show with that name.")
  else:
      # API error
      bot.send_message(message.chat.id, "Sorry, something went wrong. Please try again later.")

@bot.message_handler(commands=["subscribe"])
def subscribe_command(message):
  # Subscribe the user to a show by its id
  user_id = message.from_user.id
  try:
      # Get the show id from the message
      show_id = int(message.text.split(maxsplit=1)[-1])
      # Get the show info from the API
      show = get_show_info(show_id)
      if show:
          # Subscribe the user to the show in the database
          subscribe(user_id, show_id)
          # Send a confirmation message
          bot.send_message(message.chat.id, f"You have subscribed to {show['name']}. You will receive notifications when new episodes are airing.")
      else:
          # Invalid show id
          bot.send_message(message.chat.id, "Sorry, I could not find any show with that id.")
  except ValueError:
      # Invalid input
      bot.send_message(message.chat.id, "Please enter a valid show id. For example: /subscribe 82")

@bot.message_handler(commands=["unsubscribe"])
def unsubscribe_command(message):
  # Unsubscribe the user from a show by its id
  user_id = message.from_user.id
  try:
      # Get the show id from the message
      show_id = int(message.text.split(maxsplit=1)[-1])
      # Get the show info from the API
      show = get_show_info(show_id)
      if show:
          # Unsubscribe the user from the show in the database
          unsubscribe(user_id, show_id)
          # Send a confirmation message
          bot.send_message(message.chat.id, f"You have unsubscribed from {show['name']}. You will no longer receive notifications for this show.")
      else:
          # Invalid show id
          bot.send_message(message.chat.id, "Sorry, I could not find any show with that id.")
  except ValueError:
      # Invalid input
      bot.send_message(message.chat.id, "Please enter a valid show id. For example: /unsubscribe 82")
      
@bot.message_handler(commands=["subscriptions"])
def subscriptions(message):
  # Show the user their current subscriptions
  user_id = message.from_user.id
  # Get the list of shows that the user is subscribed to from the database
  show_ids = get_subscriptions(user_id)
  if len(show_ids) > 0:
      # Send a message for each subscribed show with its next episode info
      for show_id in show_ids:
          # Get the show info from the API
          show = get_show_info(show_id)
          if show:
              message = f"You are subscribed to {show['name']}.\n"
              # Get the next episode info from the API
              episode = get_next_episode(show_id)
              if episode:
                  message += f"The next episode is:\n"
                  message += format_episode_info(episode)
              else:
                  message += f"There is no next episode scheduled yet."
              bot.send_message(message.chat.id, message, parse_mode="HTML")
  else:
      # No subscriptions found
      bot.send_message(message.chat.id, "You have not subscribed to any shows yet. To subscribe to a show, send /subscribe [show id]. To search for a show by name, send /search [show name].")

@bot.message_handler(commands=["next"])
def next(message):
  # Show the user the next episode of a show by its id
  try:
      # Get the show id from the message
      show_id = int(message.text.split(maxsplit=1)[-1])
      # Get the next episode info from the API
      episode = get_next_episode(show_id)
      if episode:
          # Send a message with the episode info
          message = format_episode_info(episode)
          bot.send_message(message.chat.id, message, parse_mode="HTML")
      else:
          # No next episode found
          bot.send_message(message.chat.id, "Sorry, there is no next episode scheduled for this show yet.")
  except ValueError:
      # Invalid input
      bot.send_message(message.chat.id, "Please enter a valid show id. For example: /next 82")

@bot.message_handler(commands=["help"])
def help(message):
  # Show the user how to use the bot again
  start(message)

bot.polling()
      
