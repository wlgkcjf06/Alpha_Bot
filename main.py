import asyncio
import discord
from discord.ext import commands
from dice import *
import youtube_dl
f=open("D:/token/token.txt",'r')
line=f.read()




intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$",intents=intents)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.command()
async def hello(ctx):
    await ctx.send("안녕하세요!")


@bot.command()
async def dice(ctx):
    result, _color, bot, user = dice()
    embed = discord.Embed(title="주사위 게임 결과", color=_color)
    embed.add_field(name="봇의 숫자", value=":game_die:"+bot, inline=True)
    embed.add_field(name=ctx.author.name+"의 숫자", value=":game_die:"+user, inline=True)
    embed.set_footer(text="결과:"+result)
    await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("음성채널에 우선 입장해주세요.")


@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("connected to the voice channel, " + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))



@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()


@bot.command()
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("already paused")


@bot.command()
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("already playing")


@bot.command()
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
    else:
        await ctx.send("not playing")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("오류:명령어를 찾을 수 없습니다")


bot.run(line.strip()) #토큰