import discord
import os
from flask import Flask
from threading import Thread

# نظام البقاء أونلاين لـ Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات البوت
intents = discord.Intents.default()
intents.voice_states = True  # مهم لدخول الروم
client = discord.Client(intents=intents)

# رقم الروم الصوتي حقك
VOICE_CHANNEL_ID = 1489192779321049199 

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Done! Connected to {channel.name}')
        except Exception as e:
            print(f'Voice Error: {e}')

keep_alive()
# تأكد إن الاسم في Environment بـ Render هو discord_token
token = os.environ.get('discord_token')
if token:
    client.run(token)
else:
    print("No token found!")
