import discord
from discord.ext import commands
import youtube_dl

client = commands.Bot(command_prefix = "/")

music_queue = []
is_playing = []
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format' : "bestaudio"}

#///////////////////////////////////////////////////

@client.command()
async def join(ctx) :

    if (ctx.author.voice is None) : # if user not in vc
        await ctx.send("youre not in vc")

    vc = ctx.author.voice.channel
    if (ctx.voice_client is None) : # if bot not in vc
        await vc.connect()
    else : # if bot in another vc
        await ctx.voice_client.move_to(vc)


@client.command()
async def disconnect(ctx) :
    await ctx.voice_client.disconnect()


@client.command()
async def play(ctx, url) :

    # create a queue/playlist
    global music_queue, is_playing
    global FFMPEG_OPTIONS, YDL_OPTIONS

    # joins vc
    vc = ctx.author.voice.channel
    if (ctx.voice_client is None) :
        if (ctx.voice_client is None) : # if bot not in vc
            await vc.connect()
        else : # if bot in another vc
            await ctx.voice_client.move_to(vc)

    # youtube_dl magic
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl :
        info = ydl.extract_info(url, download = False)
        url_a = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url_a, **FFMPEG_OPTIONS)
        
        music_queue.append(source) # add to queue
    
    # add to is_playing
    if (len(is_playing) == 0) :
        is_playing.append(music_queue[0])
        music_queue.pop(0)
        (ctx.voice_client).play(is_playing[0])


@client.command()
async def pause(ctx) :
    global music_queue, is_playing

    if (len(is_playing) == 1) :
        await ctx.voice_client.pause()
        await ctx.send("paused")
    else :
        await ctx.send("nothing to pause")


@client.command()
async def resume(ctx) :
    global music_queue, is_playing

    if (len(is_playing) == 1) :
        await ctx.voice_client.resume()
        await ctx.send("resumed")
    else :
        await ctx.send("nothing to resume")


@client.command()
async def skip(ctx) :
    global music_queue, is_playing

    if (len(is_playing) == 0) :
        await ctx.send("nothing to skip!") 

    elif (len(music_queue) > 0) :
        ctx.voice_client.stop()
        await ctx.send("skipped!")

        is_playing.append(music_queue[0])
        music_queue.pop(0)
        (ctx.voice_client).play(is_playing[0])



client.run("")


