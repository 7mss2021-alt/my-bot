import discord
from discord.ext import commands
import os
import asyncio
from flask import Flask
from threading import Thread

# --- كود البقاء حياً (Keep Alive) لضمان عدم توقف Render ---
app = Flask('')
@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------------------

# الإعدادات الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# جلب البيانات من "الخزنة" (Environment Variables) في Render
VOICE_CHANNEL_ID = 1489005300911444050 # الرقم اللي بالصورة
TOKEN = os.environ.get('discord_token')

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح باسم: {bot.user}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f"دخلت الروم بنجاح: {channel.name}")
        except Exception as e:
            print(f"خطأ في دخول الروم: {e}")
    else:
        print("لم يتم العثور على الروم، تأكد من الـ ID")

# تشغيل السيرفر الوهمي والبوت
if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("خطأ: التوكن غير موجود في إعدادات Render (discord_token)")
