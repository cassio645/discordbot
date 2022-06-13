import discord
from discord.ext import commands
from random import randint
from asyncio import TimeoutError

from pymongo import MongoClient
from decouple import config

from .funcoes import get_id, get_prefix, pass_to_money
from db.eventdb import add_milho

prefix = get_prefix()

MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Discord"]
collection = db["msg"]

levels = [
    10, 100, 200, 300, 500, 800, 1300, 2100, 3400, 5500, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000, 105000, 110000, 115000, 120000, 125000, 130000, 135000, 140000, 145000, 150000, 155000, 160000, 165000, 170000, 175000, 180000, 185000, 190000, 195000, 200000, 205000, 210000, 215000, 220000, 225000, 230000, 235000, 240000, 245000, 250000, 255000, 260000, 265000, 270000, 275000, 280000, 285000, 290000, 295000, 300000, 305000, 310000, 315000, 320000, 325000, 330000, 335000, 340000, 345000, 350000, 400000, 410000, 420000, 430000, 440000, 450000, 460000, 470000, 480000, 490000, 500000, 510000, 520000, 530000, 540000, 550000, 560000, 570000, 580000, 590000, 600000, 700000, 800000, 900000, 1000000
]

def level_up(user_id, level):
    user = collection.find_one({"_id": user_id})
    level += 1
    update_level = { "$set": {"level": level}}
    collection.update_one(user, update_level)

def get_xp_rank():
    registers = list()
    # consulta o rank por completo e ordena pela ordem de xp
    for i in collection.find({"level": {"$gt": 0}}).sort("level", -1):
        registers.append(i)
    return registers

def get_xp_user(user_id):
    try:
        info = collection.find_one({"_id": user_id})
        level = "Level " + str(info["level"])
        xp = str(pass_to_money(info['xp'])) +"/"+ str(pass_to_money(levels[info['level']])) + "xp"
        return level, xp
    except: return "0", "0/10"

def delete_xp(user_id):
    # apaga os dados de um usuário
	try:
		collection.delete_one({"_id": user_id})
	except:
		pass


class Rank(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        user_id = ctx.author.id
        if ctx.author.bot: return
        #if user_id: return
        xp = randint(1, 5)
        num = randint(1, 100)
        if num >= 75:
            users = set()
            await ctx.add_reaction("\U0001f33d")
            def check_reaction(reaction, user):
                if str(reaction.emoji)=="\U0001f33d" and reaction.message==ctx:
                    users.add(user)
                    return False
            try:
                await self.bot.wait_for("reaction_add", check=check_reaction, timeout=30)
            except TimeoutError:
                pass
            add_milho(users)


        if collection.find_one({"_id": user_id}):
            user = collection.find_one({"_id": user_id})
            newxp = (user["xp"]) + xp
            newvalues = { "$set": {"xp": newxp}}
            collection.update_one(user, newvalues)
            if newxp >= levels[user['level']]:
                level_up(user_id, user['level'])
                #channel = self.bot.get_channel(972213997833187408)
                #await channel.send(f"<@{user_id}> subiu para o level {user['level'] + 1}")
        else:
            dados = {"_id": user_id, "level": 0, "xp": xp}
            collection.insert_one(dados)

    @commands.command(name="reset_xp", aliases=["reset-xp", "resete-xp", "resete_xp"])
    @commands.has_permissions(administrator=True)
    async def reset_xp(self, ctx):
        if collection.delete_many({"xp": {"$gt": 0}}):
            await ctx.send("O xp do servidor foi resetado.")
        else:
            await ctx.send("Não foi.")




def setup(bot):
    """Load Rank Cog."""
    bot.add_cog(Rank(bot))