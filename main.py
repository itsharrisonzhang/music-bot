import discord
from discord.ext import commands


client = commands.Bot(command_prefix = ".")

@client.command()
async def play(ctx, url : str) :

    # replace General with name of vc the user is in
    vc = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if (not voice.is_connected()) :
        await vc.connect()

@client.command()
async def leave(ctx) :
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




