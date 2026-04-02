import discord
import os
from flask import Flask
from threading import Thread

# سيرفر Keep Alive للبقاء أونلاين
app = Flask('')
@app.route('/')
def home(): return "Online"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

intents = discord.Intents.default()
intents.voice_states = True 
client = discord.Client(intents=intents)

# تأكد من رقم الروم الصوتي حقك
VOICE_CHANNEL_ID = 1489192779321049199 

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f'Done! Joined: {channel.name}')
        except Exception as e:
            print(f'Voice Error: {e}')

keep_alive()
# سحب التوكن من Render
token = os.environ.get('discord_token')
if token:
    try:
        client.run(token)
    except discord.errors.LoginFailure:
        print("Error: The token provided is invalid!")
else:
    print("Error: discord_token variable not found!")
