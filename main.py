import os
from decouple import config
from discord import Intents
from discord.ext import commands

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='k!', case_insensitive=True, intents=intents, strip_after_prefix=True)
bot.remove_command('help')

bot.load_extension("manager")
bot.load_extension("code.help")
bot.load_extension("code.utils")
bot.load_extension("code.connect_four")
bot.load_extension("code.economy")
bot.load_extension("code.store")
bot.load_extension("code.casino")
bot.load_extension("code.profile")
bot.load_extension("code.rank_xp")
bot.load_extension("code.game")


TOKEN = config("TOKEN")

bot.run(TOKEN)
