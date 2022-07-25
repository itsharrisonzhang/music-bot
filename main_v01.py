from operator import truediv
import discord
from discord.ext import commands
import youtube_dl
from time import *
import threading

client = commands.Bot(command_prefix = "/")

music_queue = []
queue_durations = []
is_playing = []
current_duration = []

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format' : "bestaudio"}

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
    global music_queue, is_playing, start, end
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
            music_queue.append(source) # add music to queue
            queue_durations.append(duration) # add duration to queue
        
        # add music to is_playing
        if (len(music_queue) == 1) :
            is_playing.append(music_queue[0])
            current_duration.append(queue_durations[0])
            music_queue.pop(0)
            queue_durations.pop(0)

        while (len(is_playing) != 0) :

            if (len(music_queue) == 0) :
                ctx.voice_client.play(is_playing[0])
                time_music(current_duration[0]) 
            
            else : # if queue length is not 0
                is_playing.append(music_queue[0])
                current_duration.append(queue_durations[0])
                music_queue.pop(0)
                queue_durations.pop(0)

                ctx.voice_client.play(is_playing[0])
                time_music(current_duration[0])



def time_music (duration) :
    for n in range(int(duration + 1.0)) :
        duration = duration - 1
        sleep(1)

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

client.run("")


