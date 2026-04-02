import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from flask import Flask
from threading import Thread

# 1. تشغيل سيرفر ويب بسيط عشان Render ما يطفي البوت
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# 2. إعدادات الصوت - تم إجبار البوت على استخدام ساوند كلاود فقط
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'scsearch', # البحث في ساوند كلاود (هنا السر)
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
        # هنا البوت بيبحث في ساوند كلاود وما راح ينحجب
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# 3. إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# 4. أمر التشغيل - يدخل الروم فوراً
@bot.command(name='play')
async def play(ctx, *, search):
    if not ctx.author.voice:
        return await ctx.send("ادخل روم صوتي أول يا بطل!")
    
    # يدخل الروم أول شيء قبل البحث عشان ما يعلق
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
    
    await ctx.send(f"🔍 جاري البحث عن: **{search}** في SoundCloud...")

    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(search, loop=bot.loop, stream=True)
            vc.play(player)
            await ctx.send(f'🎵 بدأ التشغيل: **{player.title}**')
        except Exception as e:
            await ctx.send(f"❌ تعذر التشغيل من ساوند كلاود أيضاً، جرب اسم ثاني. الخطأ: {e}")

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("تم الإيقاف! 👋")

# 5. تشغيل كل شيء
keep_alive()
token = os.environ.get('discord_token')
bot.run(token)
