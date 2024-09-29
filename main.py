import os
import discord
from discord.ext import commands
from flask import Flask
import threading

# Set up the bot with the necessary intents to monitor messages and message deletion
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to read message content
intents.messages = True  # Enables message events like on_message and on_message_delete

bot = commands.Bot(command_prefix="!", intents=intents)

# Simple web server to keep Replit active
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# Log all messages to a file
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Log message content to a file
    with open("messages_log.txt", "a") as f:
        f.write(f"{message.author}: {message.content} (in {message.channel})\n")
    await bot.process_commands(message)

# Log deleted messages to a file
@bot.event
async def on_message_delete(message):
    with open("deleted_messages_log.txt", "a") as f:
        f.write(f"Deleted message from {message.author}: {message.content} (in {message.channel})\n")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Run the bot and the web server in parallel
def run_bot():
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))

# Start the web server in a separate thread
threading.Thread(target=run_web_server).start()

# Run the bot
run_bot()
