import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# سيرفر وهمي عشان Render ما يطفي البوت
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# حط الـ ID حق الروم هنا
VOICE_CHANNEL_ID = 1489192779321049199

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f"دخلت الروم: {channel.name}")
        except Exception as e:
            print(f"خطأ في الدخول: {e}")

# تشغيل البوت باستخدام التوكن من "البيئة"
keep_alive()
TOKEN = os.environ.get('discord_token')
if TOKEN:
    bot.run(TOKEN)
