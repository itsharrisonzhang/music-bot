import discord
from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix = "/")
music_queue = {}

vc_name = ""

@client.command()
async def join(ctx) :
    global vc_name

    if (ctx.author.voice is None) : # if user not in vc
        await ctx.send("youre not in vc")
    elif (not ctx.author.voice is None ) :
        vc_name = str(ctx.author.voice.channel.name)

    vc = ctx.author.voice.channel
    if (ctx.voice_client is None) : # if bot not in vc
        await vc.connect()
    else : # if bot in another vc
        await ctx.voice_client.move_to(vc)



@client.command()
async def disconnect(ctx) :
    await ctx.voice_client.disconnect()



@client.command()
async def play(ctx) :

    # create a queue/playlist
    #stream directly from youtube

    # replace General with name of vc the user is in
    
    vc_name = str(ctx.author.voice.channel.name)
    if (vc_name != None) :
        await voice.connect()
        await ctx.send("hi!!!")
    else : pass

    vc = discord.utils.get(ctx.guild.voice_channels, name = ctx.author.voice.channel.name)

    try :
        await voice.connect()
        await ctx.send("hi!!!")

    except Exception :
        await ctx.send("I'm already in call!")

    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)








@client.command()
async def leave(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    try :
        await voice.disconnect()

    except Exception :
        await ctx.send("I'm not in call.")

client.run("")



