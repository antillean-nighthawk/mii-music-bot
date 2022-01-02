# a discord music bot that does nothing but play an uncomfortable version of the mii channel theme nonstop
# some of the code is based off of https://github.com/eric-yeung/Discord-Bot/blob/master/main.py
# and https://github.com/DivyaKumarBaid/Discord_Music_bot/blob/main/main.py
# and https://github.com/JuicyM/Radio-Kappa/blob/master/kappabot.py


import os, discord
#from discord.utils import _get_as_snowflake
#from discord import TextChannel
from discord.ext import commands, tasks
from discord.player import FFmpegPCMAudio
from dotenv import load_dotenv
from youtube_dl import YoutubeDL

load_dotenv()
client = commands.Bot(command_prefix='!', description="Mii music nonstop >:)")

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YT_COLOR = 0xc4302b
YT_ICON = "https://www.youtube.com/yt/brand/media/image/YouTube-icon-full_color.png"
AUTHOR_ICON = "https://yt3.ggpht.com/ytc/AKedOLSa4RDh1BOLfifSMLLZD2wGf35Tk4DIUvo3xlXZnQ=s88-c-k-c0x00ffffff-no-rj"
AUTHOR_CHANNEL = "https://www.youtube.com/channel/UCjyeRhvCylsaY0JrrTjrEvw"
MII_THEME = "https://www.youtube.com/watch?v=3q7oJuyy5Ac"
with YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(MII_THEME, download=False)
    URL = info['url']

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@tasks.loop(seconds=1)
async def play_song(ctx, channel, voice, user):
    if not voice.is_playing():
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        if user not in channel.members:
            await voice.disconnect()

@client.command(pass_context= True, no_pm=True, help="Play song")
async def play(ctx):
    channel = ctx.message.author.voice.channel
    user = ctx.message.author
    await channel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    play_song.start(ctx, channel, voice, user)
    await ctx.send('Playing mii channel theme but all the pauses are uncomfortably long')

@client.command(pass_context=True, no_pm=True, help="Song details")
async def description(ctx):
    em = discord.Embed(title="mii channel but all the pauses are uncomfortably long", url=MII_THEME, description="endless fun", colour=YT_COLOR )
    em.set_author(name="Odessa Marston", url=AUTHOR_CHANNEL, icon_url=AUTHOR_ICON)
    em.set_thumbnail(url=YT_ICON)
    em.add_field(name="Duration", value="infinite", inline=True)
    em.add_field(name="Views", value="8,088,023", inline=True)
    em.add_field(name="Likes", value="315K", inline=True)
    em.add_field(name="Dislikes", value="None", inline=True)
    await ctx.send(embed=em)

@client.command(pass_context=True, no_pm=True, help="Try and stop it")
async def stop(ctx):
    await ctx.send("Hahahahaha you can't stop it")

@client.command(pass_context=True, no_pm=True, help="Try again")
async def disconnect(ctx):
    await ctx.send("You wish")

@client.command(pass_context=True, no_pm=True, help="Make it stop")
async def end(ctx):
    await ctx.send("It will never end")

client.run(os.getenv('TOKEN'))
