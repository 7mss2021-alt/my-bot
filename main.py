import discord
import os
from flask import Flask
from threading import Thread

# سيرفر بسيط للبقاء حياً
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات البوت
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# رقم الروم الصوتي (تأكد إنه ID صحيح)
VOICE_CHANNEL_ID = 1378484001668599859

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Successfully joined: {channel.name}')
        except Exception as e:
            print(f'Voice Error: {e}')

keep_alive()

# جلب التوكن وتشغيل البوت
token = os.environ.get('discord_token')
if token:
    client.run(token)
else:
    print("TOKEN NOT FOUND!")
