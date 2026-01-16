import discord                                                          #Imports discord.py
from discord.ext import commands                                        #Imports the command ability
from discord.ext.commands import has_permissions, MissingPermissions    #Imports permission conditions
from discord import FFmpegPCMAudio                                      #Imports the ability to play audio
from discord import Member                                              #Imports the members
import requests                                                         #Imports the ability to request to an API
from apikeys import *                                                   #API's stored

intents = discord.Intents.default()                                     #Makes the default config of discord to read messages
intents.message_content = True                                          #Can check messages

queues = {}                                                             #The dictionary of songs queued

def check_queue(ctx, guild_id):                                                                  #Def of checking if queue has songs
    if queues[guild_id] != []:                                                                   #If there are...
        voice = ctx.guild.voice_client                                                           #Connect to the voice channel
        source = queues[guild_id].pop(0)                                                         #Selects the first song of the list and eliminates it
        player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id)) #Plays the song and schedules the next queue check

bot = commands.Bot(command_prefix="!", intents=intents)                                          #The prefix used to use commands is !

#Bot joined
@bot.event
async def on_ready():                                                                           #When the bot is ready
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Moderando")) #Changes status             #discord.Streaming(name="Game", url="") 
    print(f"Estamos dentro! {bot.user}")                                                        #Logs that it's online and it's username

#Pokemon pic command
@bot.command()
async def poke(ctx, arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        result = requests.get(POKE+pokemon)
        if result.text == "Not Found":
            await ctx.send("Pokemon no Encontrado")
        else:
            image_url = result.json()["sprites"]["front_default"]
            await ctx.send(image_url)

    except Exception as e:
        print("Error: ", e)

@poke.error                                                             #When there's an error when typing the command...
async def error_type(ctx, error):                                       #Defines error
    if isinstance(error, commands.errors.MissingRequiredArgument):      #When you missed an argument...
        await ctx.send("Tienes que pasarme un Pokemon")                 #It will send instructions on how to proceed

#Clean-up
@bot.command()
async def limpiar(ctx):                                     #!limpiar
    await ctx.channel.purge()                               #Deletes channel messages
    await ctx.send("Mensajes eliminados", delete_after=3)   #Notifies it and deletes it's own message after 3 sec

#VC-Music
@bot.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("WTP.mp3")
        player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))    #Plays the song and schedules the next queue check

    else:
        await ctx.send("Tienes que estar en un canal de voz")

@bot.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Me voy")
    else:
        await ctx.send("No estoy en un canal de voz")

@bot.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No hay audio reproduciendose en el chat de voz ahora mismo")
    
@bot.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("No hay ninguna canción pausada")

@bot.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients,guild=ctx.guild)
    voice.stop()

@bot.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + ".mp3"
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))    #Plays the song and schedules the next queue check

#Music queuer
@bot.command(pass_context = True)                       #Has context
async def queue(ctx, arg):                              #!queue
    voice = ctx.guild.voice_client                      #It will acces the voice channel
    song = arg + ".mp3"                                 #The song wiil be the title written + the ussual extension
    source = FFmpegPCMAudio(song)                       #It will use FFMPEG as an audio player

    guild_id = ctx.message.guild.id                     #It gathers the information provided

    if guild_id in queues:                              #If the information is in the queues
        queues[guild_id].append(source)                 #Adds the song

    else:                                               #Else
        queues[guild_id] = [source]                     #Won't add the song

    await ctx.send("Añadido a la lista de siguiente")   #Notify the sucess

#Word Moderation
@bot.event
async def on_message(message):                                                  #When a message is received...
    if message.author == bot.user:                                              #If the bot wrote a forbidden word, nothing happens
        return
    
    if "gilipollas" in message.content.lower():                                 #If a message contains this words...
        await message.delete()                                                  #It will be deleted
        await message.channel.send("No digas eso")                              #And will be warned
        print(f"Message received: '{message.content}' from {message.author}")   #Notifies to me in the logs
        
    await bot.process_commands(message)                                         #Processes other events and command

#Kick
@bot.command()
@has_permissions(kick_members=True)                         #If you have the permission to kick people it will let you use this command
async def kick(ctx, member: discord.Member, *, reason=None):#!kick
    await member.kick(reason=reason)                        #Kicks account
    await ctx.send(f"El usuario {member} ha sido kickeado") #Notifies the server in that channel

#Ban
@bot.command()
@has_permissions(ban_members=True)                          #If you have the permission to ban people it will let you use this command
async def ban(ctx, member: discord.Member, *, reason=None): #!ban
    await member.ban(reason=reason)                         #Bans account
    await ctx.send(f"El usuario {member} ha sido baneado")  #Notifies the server in that channel

#Embedded text
@bot.command()
async def twitch(ctx):                                                  #!twitch
    embed = discord.Embed(title="Estoy en directo en Twitch", url="https://twitch.tv/elj28gamer", description="Vamos a jugar a Balatro, Chess y Geometry Dash", color=0x71368a) #Title, Desciption, Color and URL
    embed.set_author(name="ElJ28Gamer", url="https://twitch.tv/elj28gamer", icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/b4b7f031-9672-4d7e-a171-0372c4fca318-profile_image-70x70.png") #Nombre puede ser ctx.author.display_name y el icono es ctx.author.avatar_url
    embed.add_field(name="Hora española", value="18:00", inline=True)   #Section 1
    embed.set_footer(text="Hasta la próxima!")                          #Foot note
    await ctx.send(embed=embed)                                         #Message sent

#Error
@bot.event
async def on_command_error(ctx, error):                             #When there is an error in a command...
    if isinstance(error, commands.errors.MissingPermissions):              #And the error is from not having permissions...
        await ctx.send("No tienes permisos para usar este comando") #You will be notified about it

bot.run(D_TOKEN)