import discord
from discord.ext import commands
import asyncio
import os

from apikeys import DISCORD_TOKEN

intents = discord.Intents.default()                                     #Makes the default config of discord to read messages
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = []

#Bot joined
@bot.event
async def on_ready():                                                                           #When the bot is ready
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Moderando")) #Changes status             #discord.Streaming(name="Game", url="") 
    print(f"Estamos dentro! {bot.user}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extensions.append(f"cogs.{filename[:-3]}")

if __name__ == "__main__":
    async def load_extensions():
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                print(f"Extensión {extension} cargada con éxito") # Información adicional para depuración
            except Exception as e:
                print(f"No se pudo cargar {extension}: {e}") # Las fuentes sugieren capturar errores para saber qué falló
    
    async def main():
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

    asyncio.run(main())