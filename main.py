import discord
from discord.ext import commands
import asyncio

# 1. الإعدادات الأساسية
intents = discord.Intents.default()
intents.message_content = True 
intents.voice_states = True    

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. حط هنا الـ ID حق الروم الصوتي اللي تبيه
VOICE_CHANNEL_ID = 1489005300911444050  # <--- امسح الرقم هذا وحط الـ ID حقك

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت باسم: {bot.user}')
    
    # محاولة الدخول للروم تلقائياً عند التشغيل
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print(f"تم الدخول بنجاح لروم: {channel.name}")
        except Exception as e:
            print(f"خطأ في الدخول للروم: {e}")
    else:
        print("لم يتم العثور على الروم، تأكد من الـ ID!")

# 3. حط التوكن حقك هنا
bot.run('MTQ4OTAwNTk2NDc4MTgxNzk5Nw.Gppcve.4YqkDzkW5q0kFYz52uLl6duwZIyt4I50PE7EHA')