import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import os

# --- التوكن من Render ---
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise Exception("TOKEN not found! حطه في Render Environment Variables")

# --- ايدي الروم الصوتي ---
VOICE_CHANNEL_ID = 1489192779321049199  # غيره لو تبي

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Web server (عشان Render ما ينام) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- عند تشغيل البوت ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not stay_connected.is_running():
        stay_connected.start()

# --- يخليه 24/7 في الروم ---
@tasks.loop(seconds=20)
async def stay_connected():
    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel is None:
        print("Channel not found!")
        return

    vc = channel.guild.voice_client

    try:
        # إذا مو داخل → يدخل
        if vc is None:
            vc = await channel.connect()

        # إذا في روم ثاني → يرجع
        elif vc.channel.id != VOICE_CHANNEL_ID:
            await vc.move_to(channel)

        # يخليه دفن بدون ميوت
        await channel.guild.change_voice_state(
            channel=channel,
            self_deaf=True,
            self_mute=False
        )

    except Exception as e:
        print(f"Error: {e}")

# --- تشغيل ---
keep_alive()
print("Bot is starting...")
bot.run(TOKEN)
