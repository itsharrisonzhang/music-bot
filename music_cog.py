from curses.panel import bottom_panel
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        
        # state of bot
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []

        # audio
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnected_streamed 1 -reconnect_delay_max_5', 'options': '-vn'}

        self.vc = None
    
    def search_yt (self, item) :
        with YoutubeDL(self.YDL_OPTIONS) as ydl :
            try :
                # search for music
                info = ydl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]

            except Exception :
                return False

        # return entries/url for music
        return {'source': info['formats'[0]['url']], 'title': info['title']}

    def play_next (self) :
        if len(self.music_queue) > 0 :
            self.is_playing = True

            url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegAudio(url, **self.FFMPEG_OPTIONS), after =lambda e: self.play_next())
        
        else :
            self.is_playing = False




