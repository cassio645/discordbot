import discord
from discord.ext import commands
from random import randint, choice
from asyncio import TimeoutError

from pymongo import MongoClient
from decouple import config

from .funcoes import get_id, get_prefix, pass_to_money
from db.eventdb import add_milho_users

prefix = get_prefix()

MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["msg"]

levels = [
    10, 100, 200, 300, 500, 800, 1300, 2100, 3400, 5500, 7700, 10000, 12400, 14900, 17500, 20200, 23000, 25900, 28900, 32000, 35200, 38500, 41900, 45400, 49000, 52700, 56500, 60400, 64400, 68500, 72700, 77000, 81400, 85900, 90500, 95200, 100000, 104900, 109900, 115000, 120200, 125500, 130900, 136400, 142000, 147700, 153500, 159400, 165400, 171500, 177700, 184000, 190400, 196900, 203500, 210200, 217000, 223900, 230900, 238000, 245200, 252500, 259900, 267400, 275000, 282700, 290500, 298400, 306400, 314500, 322700, 331000, 339400, 347900, 356500, 365200, 374000, 382900, 391900, 401000, 410200, 419500, 428900, 438400, 448000, 457700, 467500, 477400, 487400, 497500, 507700, 518000, 528400, 538900, 549500, 560200, 571000, 581900, 592900, 604000 
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
        xp = [0, 0, 1, 2, 5, 10]
        xp = choice(xp)

        # evento
        num = randint(1, 1000)
        if num <= 60:
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
            add_milho_users(users) # end evento

        if xp > 0:
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


'''
    @commands.command(name="reset_xp", aliases=["reset-xp", "resete-xp", "resete_xp"])
    @commands.has_permissions(administrator=True)
    async def reset_xp(self, ctx):
        if collection.delete_many({"xp": {"$gt": 0}}):
            await ctx.send("O xp do servidor foi resetado.")
        else:
            await ctx.send("Não foi.")
'''



def setup(bot):
    """Load Rank Cog."""
    bot.add_cog(Rank(bot))