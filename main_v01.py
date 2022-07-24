import discord
from discord.ext import commands
import youtube_dl
import os

client = commands.Bot(command_prefix = ".")
music_queue = {}


@client.command()
async def play(ctx) :
    
    # create a queue/playlist
    #stream directly from youtube

    # replace General with name of vc the user is in
    vc = discord.utils.get(ctx.guild.voice_channels, name = ctx.author.voice.channel.name)
    
    await vc.connect()
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    await ctx.send("hi!!!")


@client.command()
async def leave(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    try :
        await voice.disconnect()
    except Exception :
        await ctx.send("I'm no longer in call :pensive:")

@client.command()
async def pause(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    try :
        await voice.pause()
    except Exception :
        await ctx.send("Audio is already paused.")

@client.command()
async def resume(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    try :
        await voice.resume()
    except Exception :
        await ctx.send("Audio is already playing.")

@client.command()
async def stop (ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    voice.stop()

@client.command()
async def queue (ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

client.run("redacted")



