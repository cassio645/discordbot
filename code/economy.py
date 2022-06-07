import discord
import time
from random import randint
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from db.mydb import get_balance, add_money, get_daily, add_daily
from .funcoes import pass_to_money, get_days, get_prefix, get_id, all_channels

prefix = get_prefix()


class Economy(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.channels = all_channels()

	@commands.command(name="balance", aliases=["diamantes", "money", "cash", "bal", "dinheiro", "kivs"])
	async def balance(self, ctx):
		if ctx.channel.id in self.channels:
			dinheiro = get_balance(ctx.author.id)
			money = pass_to_money(dinheiro)
			daily_embed = discord.Embed(title=" ", description=f"**Kivs**: {money} :drop_of_blood: ", colour=0xFFD301)
			await ctx.send(embed=daily_embed)


	@commands.command()
	async def daily(self, ctx):
		if ctx.channel.id in self.channels:
			today = get_days()
			date = get_daily(ctx.author.id)
			if date < today:
				valor_daily = randint(1000, 3550)
				daily_embed = discord.Embed(title=" ", description=f"**Você recebeu**: {valor_daily} :drop_of_blood: ", colour=0xFFD301)
				add_daily(ctx.author.id, money=valor_daily, daily=today)
				await ctx.send(embed=daily_embed)
			else:
				await ctx.send(f"Você já pegou seu daily hoje.")



	@commands.command(name="pay", aliases=["pagar", "send", "pagamento", "enviar"])
	@commands.has_permissions(administrator=True)
	async def pay(self, ctx, user=None, money=None):
		if ctx.channel.id in self.channels:
			try:
				if user and money:
					if len(user) < 18 and len(money) >= 18:
						user, money = money, user
						
					user = get_id(user)
					money = int(money)
					if user and money:
						add_money(user, money)
						await ctx.send("Pagamento feito.")
					else:
						await ctx.send("Algo deu errado.")
						return
				elif user and not money:
					await ctx.send("Você não informou o valor.")
					return
				elif money and not user:
					await ctx.send("Você não informou o usuário.")
					return
				else:
					await ctx.send(f"`{prefix}pay <@membro | ID> <valor>`")
					return
			except:
				await ctx.send("Algo deu errado.")



	
	
def setup(bot):
    """Load Economy Cog."""
    bot.add_cog(Economy(bot))