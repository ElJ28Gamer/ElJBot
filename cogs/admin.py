import discord                                                                      #Import discord
from discord.ext import commands                                                    #Import commands
from discord.ext.commands import has_permissions, MissingPermissions                #Imports permission conditions
from discord import Member                                                          #Imports the members

bot = commands.Bot

class Admin(commands.Cog):                                                          #Class Admin is a command Cog

    def __init__(self, bot):                                                        #Introduces bot on init
        self.bot = bot                                                              #bot is bot from commands

    #Clean-up
    @commands.command()
    async def limpiar(self, ctx):                                                   #!limpiar
        await ctx.channel.purge()                                                   #Deletes channel messages
        await ctx.send("Mensajes eliminados", delete_after=3)                       #Notifies it and deletes it's own message after 3 sec
    
    #Word Moderation
    @commands.Cog.listener()
    async def on_message(message):                                                  #When a message is received...
        if message.author == bot.user:                                              #If the bot wrote a forbidden word, nothing happens
            return
    
        if "gilipollas" in message.content.lower():                                 #If a message contains this words...
            await message.delete()                                                  #It will be deleted
            await message.channel.send("No digas eso")                              #And will be warned
            print(f"Message received: '{message.content}' from {message.author}")   #Notifies to me in the logs
        
        await bot.process_commands(message)                                         #Processes other events and command

    #Kick
    @commands.command()
    @has_permissions(kick_members=True)                         #If you have the permission to kick people it will let you use this command
    async def kick(ctx, member: discord.Member, *, reason=None):#!kick
        await member.kick(reason=reason)                        #Kicks account
        await ctx.send(f"El usuario {member} ha sido kickeado") #Notifies the server in that channel

    #Ban
    @commands.command()
    @has_permissions(ban_members=True)                          #If you have the permission to ban people it will let you use this command
    async def ban(ctx, member: discord.Member, *, reason=None): #!ban
        await member.ban(reason=reason)                         #Bans account
        await ctx.send(f"El usuario {member} ha sido baneado")  #Notifies the server in that channel

    #Embedded text
    @commands.command()
    async def twitch(ctx):                                                  #!twitch
        embed = discord.Embed(title="Estoy en directo en Twitch", url="https://twitch.tv/elj28gamer", description="Vamos a jugar a Balatro, Chess y Geometry Dash", color=0x71368a) #Title, Desciption, Color and URL
        embed.set_author(name="ElJ28Gamer", url="https://twitch.tv/elj28gamer", icon_url="https://static-cdn.jtvnw.net/jtv_user_pictures/b4b7f031-9672-4d7e-a171-0372c4fca318-profile_image-70x70.png") #Nombre puede ser ctx.author.display_name y el icono es ctx.author.avatar_url
        embed.add_field(name="Hora española", value="18:00", inline=True)   #Section 1
        embed.set_footer(text="Hasta la próxima!")                          #Foot note
        await ctx.send(embed=embed)                                         #Message sent

    #Error
    @commands.Cog.listener()
    async def on_command_error(ctx, error):                             #When there is an error in a command...
        if isinstance(error, commands.errors.MissingPermissions):              #And the error is from not having permissions...
            await ctx.send("No tienes permisos para usar este comando") #You will be notified about it

    #DM
    @commands.command()
    async def message(ctx, user:discord.Member, *, message=None):   #!message @user
        message = "Bienvenido al servidor"
        embed = discord.Embed(title=message)                        #Prepare the embed to be the message
        await user.send(embed=embed)                                #Send the user the embed

async def setup(bot):                                                               #Setups the class
    await bot.add_cog(Admin(bot))                                                   #Introduces it on main.py