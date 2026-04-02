import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from flask import Flask
from threading import Thread

# Flask للـ Keep Alive
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# إعدادات الصوت (YouTube DL)
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
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

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name='play')
async def play(ctx, *, search):
    if not ctx.message.author.voice:
        await ctx.send("ادخل روم صوتي أول!")
        return
    
    channel = ctx.message.author.voice.channel
    vc = ctx.voice_client or await channel.connect()

    async with ctx.typing():
        player = await YTDLSource.from_url(search, loop=bot.loop, stream=True)
        vc.play(player)

    await ctx.send(f'جاري تشغيل: **{player.title}** 🎵')

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم إيقاف التشغيل.")

keep_alive()
bot.run(os.environ.get('discord_token'))
