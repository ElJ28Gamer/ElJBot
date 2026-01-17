import discord                                                      #Imports discord
from discord.ext import commands                                    #Imports commands
import asyncio                                                      #Imports async ability to start the bot
import os                                                           #Imports os for music + cogs

from apikeys import DISCORD_TOKEN                                   #Imports the discord token

intents = discord.Intents.default()                                 #Makes the default config of discord to read messages
intents.message_content = True                                      #Changes offline default to true

bot = commands.Bot(command_prefix="!", intents=intents)             #The prefix for commands is !

initial_extensions = []                                             #Extension list for the cogs

@bot.event                                                          #Bot joined event
async def on_ready():                                               #When the bot is ready
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Moderando")) #Changes status #discord.Streaming(name="Game", url="") 
    print(f"Estamos dentro! {bot.user}")                            #Prints in the logs that it is in

for filename in os.listdir("./cogs"):                               #Search files in the cogs folder...
    if filename.endswith(".py"):                                    #Whose extension is .py
        initial_extensions.append(f"cogs.{filename[:-3]}")          #Adds the cog into the initial_extension list

if __name__ == "__main__":                                          #If the name of this file is "main"...
    async def load_extensions():                                    #Defines the loading process of the extensions/cogs
        for extension in initial_extensions:                        #For each extension..
            try:                                                    #Tries to...
                await bot.load_extension(extension)                 #Load them
                print(f"Extensión {extension} cargada con éxito")   #And notify in the logs

            except Exception as e:                                  #Except there's an exception...
                print(f"No se pudo cargar {extension}: {e}")        #Which tells us that it couldn't load the extension/cog
    
    async def main():                                               #Defines the main execution of the bot
        await load_extensions()                                     #Loads the extensions previously defined
        await bot.start(DISCORD_TOKEN)                              #Starts the bot

    asyncio.run(main())                                             #Runs the bot in an asynchronous way