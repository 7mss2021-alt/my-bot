import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# سيرفر بسيط عشان Render يخلي البوت شغال 24 ساعة
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات البوت (صامتة تماماً)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- ضع هنا رقم الروم الصوتي اللي تبيه يدخله ---
VOICE_CHANNEL_ID = 1489192779321049199 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            # يحاول يدخل الروم الصوتي فور تشغيله
            await channel.connect()
            print(f'Connected successfully to: {channel.name}')
        except Exception as e:
            print(f'Failed to connect to voice: {e}')

# تشغيل البوت
keep_alive()
bot.run(os.environ.get('discord_token'))
