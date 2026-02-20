import discord
from discord.ext import commands
import os
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ======================
# JOIN
# ======================
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send("เข้าห้องแล้ว 🎵")
    else:
        await ctx.send("คุณต้องอยู่ในห้องเสียงก่อน!")

# ======================
# LEAVE
# ======================
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("ออกจากห้องแล้ว 👋")
    else:
        await ctx.send("บอทยังไม่ได้เข้าห้อง")

# ======================
# PLAY
# ======================
@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        await ctx.send("คุณต้องอยู่ในห้องเสียงก่อน!")
        return

    channel = ctx.author.voice.channel

    if not ctx.voice_client:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']

        ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio(url2))
        await ctx.send("กำลังเปิดเพลง 🎶")

    except Exception as e:
        await ctx.send("เกิดข้อผิดพลาดในการเปิดเพลง")
        print(e)

# ======================
# STOP
# ======================
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("หยุดเพลงแล้ว ⏹️")
    else:
        await ctx.send("ไม่มีเพลงกำลังเล่น")

bot.run(os.getenv("TOKEN"))
