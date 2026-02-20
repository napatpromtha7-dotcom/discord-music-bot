import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def play(ctx, *, url):
    if not ctx.author.voice:
        await ctx.send("❌ เข้าห้องเสียงก่อน")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        voice = await channel.connect()
    else:
        voice = ctx.voice_client

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

    if 'entries' in data:
        data = data['entries'][0]

    url2 = data['url']

    source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
    voice.play(source)

    await ctx.send(f"🎵 กำลังเล่น: {data['title']}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

bot.run(os.getenv("TOKEN"))
