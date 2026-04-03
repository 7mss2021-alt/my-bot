import discord
from discord.ext import commands, tasks

TOKEN = "YOUR_BOT_TOKEN"
VOICE_CHANNEL_ID = 1489192779321049199  # حط ايدي الروم الصوتي هنا

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    stay_connected.start()  # تشغيل المهمة التلقائية

@tasks.loop(seconds=30)
async def stay_connected():
    for guild in bot.guilds:
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel is None:
            continue

        vc = guild.voice_client

        # إذا البوت مو داخل الروم → يدخل
        if vc is None or not vc.is_connected():
            try:
                vc = await channel.connect()
            except:
                continue

        # يتأكد إنه بنفس الروم
        elif vc.channel.id != VOICE_CHANNEL_ID:
            await vc.move_to(channel)

        # يخليه دفن بدون ميوت
        await guild.change_voice_state(
            channel=channel,
            self_deaf=True,
            self_mute=False
        )

bot.run(TOKEN)
