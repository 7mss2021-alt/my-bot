import discord
import os
from flask import Flask
from threading import Thread

# نظام Keep Alive
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات البوت الأساسية
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# رقم الروم الصوتي حقك (تأكد إنه ID صحيح)
VOICE_CHANNEL_ID = 1489192779321049199 

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Successfully joined: {channel.name}')
        except Exception as e:
            print(f'Could not join voice: {e}')

keep_alive()
# جلب التوكن من Environment
token = os.environ.get('discord_token')
if token:
    client.run(token)
else:
    print("Token not found in Render Environment Variables!")
