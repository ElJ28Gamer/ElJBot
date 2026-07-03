import discord                                                                      #Import discord
from discord.ext import commands                                                    #Import commands
from discord import FFmpegPCMAudio                                                  #Imports the ability to play audio
from discord import Member
import random
import os                                                                           #

intents = discord.Intents.default()                                 #Makes the default config of discord to read messages
intents.message_content = True                                      #Changes offline default to true

bot = commands.Bot(command_prefix="!", intents=intents)                             #bot is the discord bot
queues = {}                                                                         #The dictionary of songs queued
music_folder = "music"

def check_queue(ctx, guild_id):                                                     #Def of checking if queue has songs
        if queues[guild_id] != []:                                                  #If there are...
            voice = ctx.guild.voice_client                                          #Connect to the voice channel
            source = queues[guild_id].pop(0)                                        #Selects the first song of the list and eliminates it
            player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id)) #Plays the song and schedules the next queue check

class Music(commands.Cog):                                                          #Class Music is a command Cog

    def __init__(self, bot):                                                        #Introduces bot on init
        self.bot = bot                                                              #bot is bot from commands
    
    @commands.command(pass_context = True)                                          #VC-Music
    async def join(self, ctx):                                                      #
        if(ctx.author.voice):                                                       #
            channel = ctx.message.author.voice.channel                              #
            voice = await channel.connect()                                         #
            if os.path.exists(music_folder):
                files = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
                if files:
                    random_file = random.choice(files)
                    source = FFmpegPCMAudio(f"{music_folder}/{random_file}")                                      #
                    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id)) #Plays the song and schedules the next queue check

        else:                                                                       #
            await ctx.send("Tienes que estar en un canal de voz")                   #

    @commands.command(pass_context = True)                                          #
    async def leave(self, ctx):                                                     #
        if(ctx.voice_client):                                                       #
            await ctx.guild.voice_client.disconnect()                               #
            await ctx.send("Me voy")                                                #

        else:                                                                       #
            await ctx.send("No estoy en un canal de voz")                           #

    @commands.command(pass_context = True)                                          #
    async def pause(self, ctx):                                                     #
        if not voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        
        voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)                #
        if voice and voice.is_playing():                                                      #
            voice.pause()                                                           #
        elif voice:
            await ctx.send("No hay canciónes reproduciendose")
        else:                                                                       #
            await ctx.send("No estoy en el canal de voz")    #
    
    @commands.command(pass_context = True)                                          #
    async def resume(self, ctx):                                                    #
        if not voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()

        voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)                #
        if voice and voice.is_paused():                                                       #
            voice.resume()                                                          #
        elif voice:
            await ctx.send("No hay ninguna canción pausada")                        #
        else:                                                                       #
            await ctx.send("No estoy en el canal de voz")
            
    @commands.command(pass_context = True)                                          #
    async def stop(self, ctx):                                                      #
        if not voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()

        voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)                #
        if voice:
            voice.stop()                                                                #
        else:
            await ctx.send("No estoy en el canal de voz")

    @commands.command(pass_context = True)                                          #
    async def play(self, ctx, arg):                                                 #
        if not ctx.author.voice:
            await ctx.send("Tienes que estar en un canal de audio")
            return
        
        voice = ctx.guild.voice_client                                              #
        if not voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()

        song_path = f"{music_folder}/{arg}.mp3"
        if os.path.exists(song_path):                                                                         #
            source = FFmpegPCMAudio(song_path)                                               #
            player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id)) #Plays the song and schedules the next queue check

    @commands.command(pass_context = True)                                          #Music queuer
    async def queue(self, ctx, arg):                                                #!queue
        if not ctx.author.voice:
            await ctx.send("Tienes que estar en un canal de audio")
            return

        voice = ctx.guild.voice_client                                              #It will acces the voice channel
        if not voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()

        song_path = f"{music_folder}/{arg}.mp3"                                                       #The song wiil be the title written + the ussual extension
        if os.path.exists(song_path):
            source = FFmpegPCMAudio(song_path)                                               #It will use FFMPEG as an audio player

            guild_id = ctx.message.guild.id                                             #It gathers the information provided

            if guild_id in queues:                                                      #If the information is in the queues
                queues[guild_id].append(source)                                         #Adds the song

            else:                                                                       #Else
                queues[guild_id] = [source]                                             #Won't add the song

            await ctx.send("Añadido a la lista de siguiente")                           #Notify the sucess

async def setup(bot):                                                               #Setups the class
    await bot.add_cog(Music(bot))                                                   #Introduces it on main.py