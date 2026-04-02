import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# نظام Keep Alive عشان الرندر ما يطفي البوت
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات البوت
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- حط رقم الروم الصوتي حقك هنا ---
VOICE_CHANNEL_ID = 1489192779321049199 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # محاولة دخول الروم فور التشغيل
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Done! Joined {channel.name}')
        except Exception as e:
            print(f'Voice Error: {e}')

keep_alive()
token = os.environ.get('discord_token')
if token:
    bot.run(token)
else:
    print("No token found in Render settings!")
