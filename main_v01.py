import discord
import youtube_dl
from discord.ext import commands
from time import *
import threading
import urllib.request, re

client = commands.Bot(command_prefix = "/")

music_queue = []
duration_queue = []
titles_queue = []
url_queue = []

is_playing = []
current_duration = []
current_title = []
current_url = []
paused = False

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format' : "bestaudio"}

#///////////////////////////////////////////////////

@client.command(name = "join", aliases = ["j"])
async def join(ctx) :
    global paused
    try :
        if (ctx.author.voice is None) : # if user is not in vc
            await ctx.send(":butterfly: | you're not in a voice channel.")
        else : 
            vc = ctx.author.voice.channel
            if (ctx.voice_client is None) : # if bot is not in vc
                await vc.connect()
            else :                          # if bot is in another vc
                await ctx.voice_client.move_to(vc)
    except Exception :
        pass

@client.command(name = "disconnect", aliases = ["dc"])
async def disconnect(ctx) :
    try :
        await ctx.voice_client.disconnect()
    except Exception :
        pass

@client.command(name = "play", aliases = ["p"])
async def play(ctx, *, search = None) :
    global music_queue, is_playing, duration_queue, current_duration, paused
    global FFMPEG_OPTIONS, YDL_OPTIONS
    try :
        # joins vc
        if (ctx.author.voice is None) : # if user is not in vc
            await ctx.send(":butterfly: | you're not in a voice channel.")
        else :
            vc = ctx.author.voice.channel
            if (ctx.voice_client is None) : # if bot is not in vc
                await vc.connect()
            else :                          # if bot is in another vc
                await ctx.voice_client.move_to(vc)
            if (paused == True) :
                ctx.voice_client.resume()

        if (search is not None) :
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl :
                search = urllib.parse.quote_plus(search, safe='')
                html  = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(search))
                url_dict = re.findall(r'watch\?v=(\S{11})', html.read().decode())
                url = 'https://www.youtube.com/watch?v=' + url_dict[0]

                info = ydl.extract_info(url, download = False)
                url_a = info['formats'][0]['url']
                duration = info['duration']
                title = info['title']
                source = await discord.FFmpegOpusAudio.from_probe(url_a, **FFMPEG_OPTIONS)
                
                music_queue.append(source)  # add music to queue
                await display_added(ctx, title, url, duration)
                print(url)
                duration_queue.append(duration) # add duration to queue
                titles_queue.append(title) # add title to queue
                url_queue.append(url) # add url to queue
                
                if (len(is_playing) == 0) :
                    func_play(ctx)
    except Exception :
        pass

def func_play(ctx) :
    global music_queue, is_playing, duration_queue, current_duration, paused, timer
    try : 
        ctx.voice_client.stop()
        is_playing.clear()
        current_duration.clear()
        current_title.clear()
        current_url.clear()

        if (len(music_queue) > 0 or len(is_playing) > 0) :
            ctx.voice_client.stop()
            is_playing.clear()
            current_duration.clear()
            current_title.clear()        
            current_url.clear()

            is_playing.append(music_queue[0])
            current_duration.append(duration_queue[0])
            current_title.append(titles_queue[0])
            current_url.append(url_queue[0])

            music_queue.pop(0)
            duration_queue.pop(0)
            titles_queue.pop(0)
            url_queue.pop(0)

            print(len(music_queue))
            ctx.voice_client.play(is_playing[0]) # after = lambda e : print('Player error: %s' % e) if e else None)
            print(current_duration[0])
            timer = threading.Timer(current_duration[0], func_play, args = [ctx])
            timer.start()
    except Exception :
        pass

async def display_added(ctx, title, url, duration) :
    queue_time = get_time(duration, 'q')
    

    embed = discord.Embed(title = ":butterfly: | added to queue [{}]".format(str(len(music_queue))), color = 0xFFFFFF) 
    embed.description = "[{}]({})".format(title, url) + " [{}]".format(get_time(duration))
    embed.set_footer(text = "total queue time: " + queue_time + "\n" + 
                            "requested by: " + ctx.author.display_name + "#" + ctx.author.discriminator)
    await ctx.send(embed = embed)

@client.command()
async def pause(ctx) :
    global paused
    try :
        if (ctx.voice_client.is_playing() and paused == False) :
            ctx.voice_client.pause()
            paused = True
            await ctx.send(":pause_button: | paused.")
        elif (paused == True) :
            await ctx.send(":pause_button: | already paused.")
        else :
            await ctx.send(":butterfly: | nothing to pause.")
    except Exception :
        await ctx.send(":butterfly: | nothing to pause.")

@client.command()
async def resume(ctx) :
    global music_queue, is_playing, paused
    try :
        if (not ctx.voice_client.is_playing() and ctx.voice_client is not None and paused == True) :
            ctx.voice_client.resume()
            paused = False
            await ctx.send(":arrow_forward: | resumed.")
        elif (paused == False) :
            pass
        else :
            await ctx.send(":butterfly: | nothing to resume.")
    except Exception :
        await ctx.send(":butterfly: | nothing to resume.")

@client.command()
async def skip(ctx, q_num = None) :
    global music_queue, is_playing, paused, timer
    try :
        if (ctx.voice_client is None or len(is_playing) == 0) :
            await ctx.send(":butterfly: | nothing to skip.") 
        else :
            paused = False
            ctx.voice_client.stop()
            timer.cancel()
            # skip to song
            skip_to = 1
            if (q_num is not None) :
                for s in range(skip_to) :
                    music_queue.pop(s)
                    duration_queue.pop(0)
                    titles_queue.pop(0)
                    url_queue.pop(0)
            if (len(music_queue) == 0) :
                new_title = ":butterfly: | skipped"
                new_desc = "nothing playing—you should queue more music!"
            else :
                new_title = ":butterfly: | skipped to [{}]".format(skip_to)
                new_desc = "**now playing: **" + titles_queue[skip_to-1] + " [{}]".format(get_time(duration_queue[skip_to-1]))
            embed = create_embed(title = new_title,
                                 description = new_desc,
                                 footer = "requested by: " + ctx.author.display_name + "#" + ctx.author.discriminator + "\n")
            await ctx.send(embed = embed)
            func_play(ctx)
    except Exception :
        await ctx.send(":butterfly: | nothing to skip.")


@client.command(name = "queue", aliases = ["q"])
async def queue(ctx) :
    global music_queue, is_playing, duration_queue, current_duration
    try : 
        q_str = ""
        if (len(is_playing) == 0 and len(music_queue) == 0) :
            q_str = ":butterfly: | nothing is playing."
            await ctx.send(q_str)
        else :
            q_str = q_str + "**now playing: **" + "[{}]({})".format(
                str(current_title[0]), current_url[0]) + " [{}]".format(get_time(current_duration[0])) + "\n\n"
            for t in range (len(titles_queue)) :
                q_str = q_str + str(t+1) + ".] " + "[{}]({})".format(
                    str(titles_queue[t]), url_queue[t]) + " [{}]".format(get_time(duration_queue[t])) + "\n"
            
            embed = create_embed(title = ":butterfly: | music queue", 
                                 description = q_str,
                                 footer = "total queue time: " + get_time(current_duration[0], 'q') + "\n")
            await ctx.send(embed = embed)
    except Exception :
        await ctx.send(":butterfly: | nothing is playing.")


def create_embed(title, description, footer, url = None) :
    if (url is None) :
        url = ""
    embed = discord.Embed(title = title, url = url, color = 0xFFFFFF)
    embed.description = description
    embed.set_footer(text = footer)
    return embed

def get_time(duration, type = None) :
    global duration_queue
    sec = duration
    if (type == 'q') :
    # get total queue duration
        for s in duration_queue :
            sec += s
    min = int(sec / 60)
    hour = int(min / 60)
    sec = sec - (min * 60 + hour * 3600)
    time_list = [hour, min, sec]
    for t in range(len(time_list)) :
        if (time_list[t] <= 9) : 
            time_list[t] = "0" + str(time_list[t])
    queue_time = ""
    if(time_list[0] == "00") :
        queue_time = str(time_list[1]) + ":" + str(time_list[2])
    else :
        queue_time = str(time_list[0]) + ":" + str(time_list[1]) + ":" + str(time_list[2])
    return queue_time

client.run("")


