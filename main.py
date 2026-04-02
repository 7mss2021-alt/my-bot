import discord
import os
from flask import Flask
from threading import Thread

# سيرفر ويب بسيط للبقاء حياً على Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات البوت
intents = discord.Intents.default()
intents.voice_states = True # ضروري لدخول الروم الصوتي
client = discord.Client(intents=intents)

# --- ضع رقم الروم الصوتي هنا ---
VOICE_CHANNEL_ID = 1378484001668599859

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Successfully joined voice channel: {channel.name}')
        except Exception as e:
            print(f'Error joining voice: {e}')

keep_alive()
# جلب التوكن من إعدادات Render
token = os.environ.get('discord_token')
if token:
    client.run(token)
else:
    print("CRITICAL: discord_token not found in Environment Variables!")
