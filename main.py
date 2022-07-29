import discord
from discord.ext import commands
import youtube_dl
import os
import hikari

client = commands.Bot(command_prefix = ".")

queue = {}


@client.command(name = "play", aliases = ["p"])
async def play(ctx, url : str) :
    
    # create a queue/playlist

    # replace General with name of vc the user is in
    vc = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if (not voice.is_connected()) :
        await vc.connect()

    ytdl_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

@client.command(name = "disconnect", aliases = ["dc"])
async def disconnect(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    
    if (voice.is_connected()) :
        await voice.disconnected()
    else :
        await ctx.send("Bot isn't connected to a vc")

@client.command()
async def pause(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if voice.is_playing() :
        voice.pause()
    else :
        await ctx.send("No audio playing")

@client.command()
async def resume(ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if voice.is_paused() :
        voice.resume()
    else :
        await ctx.send("Audio isn't paused")

@client.command()
async def stop (ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    voice.stop()

@client.command(name = "queue", aliases = ["q"])
async def queue (ctx) :
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)




