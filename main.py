import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 1. نظام الـ Keep Alive (عشان Render ما يطفي البوت)
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. إعدادات البوت
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- ضع هنا رقم الروم الصوتي اللي تبيه يدخله ---
VOICE_CHANNEL_ID = 1489192779321049199

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # أول ما يشتغل البوت، يروح يدخل الروم فوراً
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Done! Connected to: {channel.name}')
        except Exception as e:
            print(f'Error: {e}')

# 3. تشغيل البوت
keep_alive()
token = os.environ.get('discord_token')
bot.run(token)
