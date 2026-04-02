import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from flask import Flask
from threading import Thread

# 1. إعداد سيرفر Flask للبقاء حياً (Keep Alive)
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. إعدادات الصوت (تم توجيه البحث لـ SoundCloud لتفادي حجب يوتيوب)
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'scsearch', # البحث في ساوند كلاود افتراضياً
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

# 3. إعدادات البوت (تأكد من تفعيل Intents من موقع المطورين)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 4. حدث التشغيل
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# 5. أمر التشغيل المطور
@bot.command(name='play')
async def play(ctx, *, search):
    # التأكد أن المستخدم في روم صوتي
    if not ctx.author.voice:
        return await ctx.send("ادخل روم صوتي أول يا بطل!")
    
    # محاولة دخول الروم فوراً
    channel = ctx.author.voice.channel
    try:
        vc = ctx.voice_client
        if vc:
            if vc.channel != channel:
                await vc.move_to(channel)
        else:
            vc = await channel.connect()
    except
