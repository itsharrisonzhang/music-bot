import discord
from discord.ext import commands
import youtube_dl
import time

client = commands.Bot(command_prefix = "/")

music_queue = []
is_playing = []
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format' : "bestaudio"}

time_start = 0.0

#///////////////////////////////////////////////////

@client.command()
async def join(ctx) :

    if (ctx.author.voice is None) : # if user is not in vc
        await ctx.send("youre not in vc")

    vc = ctx.author.voice.channel
    if (ctx.voice_client is None) : # if bot is not in vc
        await vc.connect()
    else :                          # if bot is in another vc
        await ctx.voice_client.move_to(vc)

@client.command()
async def disconnect(ctx) :
    await ctx.voice_client.disconnect()





@client.command()
async def play(ctx, url = None) :

    # create a queue/playlist
    global music_queue, is_playing, time_start
    global FFMPEG_OPTIONS, YDL_OPTIONS

    # joins vc
    vc = ctx.author.voice.channel
    if (ctx.voice_client is None) : # if bot not in vc
        await vc.connect()
    else : # if bot in another vc
        await ctx.voice_client.move_to(vc)

    if (url is not None) :
        # youtube_dl magic
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl :
            info = ydl.extract_info(url, download = False)
            url_a = info['formats'][0]['url']
            duration = info['duration']
            source = await discord.FFmpegOpusAudio.from_probe(url_a, **FFMPEG_OPTIONS)
            music_queue.append(source) # add to queue
    
    # add to is_playing
    if (len(is_playing) == 0 or time.time() == time_start) :
        ctx.voice_client.stop()
        
        if (len(is_playing) != 0) : 
            is_playing.pop(0)
            time_start = time_start + duration + 1.0


        is_playing.append(music_queue[0])
        music_queue.pop(0)
        ctx.voice_client.play(is_playing[0])

        if (time.time() == time_start) :
            time_start = 0       







@client.command()
async def pause(ctx) :
    global music_queue, is_playing

    if (len(is_playing) == 1) :
        ctx.voice_client.pause()
        await ctx.send("paused")
    else :
        await ctx.send("nothing to pause")


@client.command()
async def resume(ctx) :
    global music_queue, is_playing

    if (len(is_playing) == 1) :
        ctx.voice_client.resume()
        await ctx.send("resumed")
    else :
        await ctx.send("nothing to resume")


@client.command()
async def skip(ctx) :
    global music_queue, is_playing

    if (len(is_playing) == 0 or ctx.voice_client is None) :
        await ctx.send("nothing to skip!") 

    else :
        ctx.voice_client.stop()
        await ctx.send("skipped!")
        is_playing.pop(0)

        if (len(music_queue) > 0) :
            is_playing.append(music_queue[0])
            music_queue.pop(0)
            ctx.voice_client.play(is_playing[0])


client.run("MTAwMDU0NDEyODYwMzU0MTYxNg.GjrYws.chEcObzYmp1lDf95fazJ7yqvqjht4uFDV0I9so")


