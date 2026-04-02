import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# نظام الـ Keep Alive
app = Flask('')
@app.route('/')
def home(): return "I am alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# رقم الروم الصوتي حقك (تأكد إنه ID روم صوتي)
VOICE_CHANNEL_ID = 1489192779321049199

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Connected to: {channel.name}')
        except Exception as e:
            print(f'Error: {e}')

keep_alive()
token = os.environ.get('discord_token')
if token:
    bot.run(token)
else:
    print("No token found in Environment Variables!")
