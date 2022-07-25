from operator import truediv
import discord
from discord.ext import commands
import youtube_dl
from time import *
import threading

client = commands.Bot(command_prefix = "/")

music_queue = []
duration_queue = []
is_playing = []
current_duration = []
time_left = 0

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
    global music_queue, is_playing
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
            duration_queue.append(duration) # add duration to queue
        
        # add music to is_playing
        if (len(is_playing) == 0 and len(music_queue) > 0) :
            is_playing.append(music_queue[0])
            current_duration.append(duration_queue[0])
            music_queue.pop(0)
            duration_queue.pop(0)

            ctx.voice_client.play(is_playing[0])
            print(current_duration[0])
            time_thread = threading.Thread(target = time_music, args = [current_duration[0] + 1])
            time_thread.start()

        while (len(music_queue) > 0) :
            if (len(is_playing) == 0) :
                
                print(current_duration[0])

                is_playing.append(music_queue[0])
                ctx.voice_client.play(is_playing[0])
                time_thread = threading.Thread(target = time_music, args = [current_duration[0] + 1])
                time_thread.start()

                # when time is up, time_music removes music from is_playing


def time_music (duration) :
    global is_playing

    duration = int(duration)
    for n in range(int(duration + 1.0)) :
        duration = duration - 1
        sleep(1)
        if (duration == 0) :
            print("0 secs")
            is_playing.pop(0)

            current_duration.pop(0)
            if (len(duration_queue) > 0) : 
                current_duration.append(duration_queue[0])

            music_queue.pop(0)
            duration_queue.pop(0)


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

client.run("MTAwMDU0NDEyODYwMzU0MTYxNg.GF3fAS.j2WCtcEqNWXf-Q43Jv7ezWVh6lm-UXFiHIIFbI")


