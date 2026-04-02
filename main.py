import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from flask import Flask
from threading import Thread

# 1. إعداد سيرفر Flask (عشان البوت ما ينام)
app = Flask('')
@app.route('/')
def home(): return "Bot is Online and Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. إعدادات الصوت (معدلة للبحث في ساوند كلاود لتجنب حجب يوتيوب)
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto', # يبحث في يوتيوب وساوند كلاود
    'source_address': '0.0.0.0'
}
ffmpeg_options = {'options': '-vn'}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# 3. إعدادات البوت والـ ID
VOICE_CHANNEL_ID = 1489192779321049199  # <--- تأكد إن هذا رقم رومك الصوتي
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 4. حدث الدخول التلقائي أول ما يشتغل البوت
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            # التحقق إذا كان البوت أصلاً في الروم عشان ما يسوي كراش
            if not bot.voice_clients:
                await channel.connect()
                print(f'Connected to voice channel: {channel.name}')
        except Exception as e:
            print(f'Error connecting to voice: {e}')

# 5. أوامر التشغيل والتحكم


@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم الإيقاف، برب!")

# 6. تشغيل كل شيء
keep_alive()
bot.run(os.environ.get('discord_token'))
