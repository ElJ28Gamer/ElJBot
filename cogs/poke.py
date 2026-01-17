import discord                                                                      #Import discord
from discord.ext import commands                                                    #Import commands
import requests                                                                     #Import API resquest

class Poke(commands.Cog):                                                           #Class Poke is a command Cog

    def __init__(self, bot):                                                        #Introduces bot on init
        self.bot = bot                                                              #bot is bot from commands

    #Pokemon pic command
    @commands.command()                                                             #commads.Cog.listener() for events
    async def poke(self, ctx, arg):                                                 #Defines !poke
        try:                                                                        #Tries...
            pokemon = arg.lower()                                                   #Sets the argument into lowercase
            result = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")   #Calls the API
            
            if result.status_code == 200:                                           #If the page status code is 200...
                image_url = result.json()["sprites"]["front_default"]               #Gets the image of the pokemon
                await ctx.send(image_url)                                           #Sends it

            elif result.status_code == 404:                                         #If the page status is 404...
                await ctx.send("Pokemon no Encontrado")                             #The pokemon is not found

            else:                                                                   #Else...
                await ctx.send("Error al buscar el Pokémon, inténtalo más tarde")   #Error because the API is down

        except Exception as e:                                                      #When it has tried and nothing happens...
            print(f"Error:  {e}")                                                   #Prints the error in the logs
            await ctx.send("Ha ocurrido un problema interno")                       #Sends message that there's a problem

    @poke.error                                                                     #When there's an error when typing the command...
    async def error_type(self, ctx, error):                                         #Defines error...
        if isinstance(error, commands.errors.MissingRequiredArgument):              #When you missed an argument
            await ctx.send("Tienes que pasarme un Pokemon")                         #It will send instructions on how to proceed

async def setup(bot):                                                               #Setups the class
    await bot.add_cog(Poke(bot))                                                    #Introduces it on main.py