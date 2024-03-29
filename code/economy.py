import discord
import time
from random import randint
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from db.mydb import get_balance, add_money, get_daily, add_daily, get_vip
from .funcoes import pass_to_money, get_days, get_prefix, get_id, all_channels

prefix = get_prefix()


class Economy(commands.Cog):
    """
    A classe Economy é uma extensão do módulo commands.Cog e fornece comandos relacionados à economia no bot.
    """

    def __init__(self, bot):
        """
        Inicializa uma nova instância da classe Economy.

        Parameters:
        bot (discord.ext.commands.Bot): O bot associado a esta classe.
        """
        self.bot = bot
        self.channels = all_channels()

    @commands.command(
        name="balance",
        aliases=["diamantes", "money", "cash", "bal", "dinheiro", "kivs", "atm"],
    )
    async def balance(self, ctx) -> None:
        f"""
        Comando para verificar o saldo de Kivs (moeda) de um usuário.

        Usage:
                {prefix}balance

        Output:
                Uma mensagem com o saldo atual de Kivs do usuário.
        """
        if ctx.channel.id in self.channels:
            dinheiro = get_balance(ctx.author.id)
            money = pass_to_money(dinheiro)
            daily_embed = discord.Embed(
                title=" ",
                description=f"**Kivs**: {money} :drop_of_blood: ",
                colour=0xFFD301,
            )
            await ctx.send(embed=daily_embed)

    @commands.command()
    async def daily(self, ctx) -> None:
        f"""
        Comando para coletar uma recompensa diária de Kivs.

        Usage:
                {prefix}daily

        Output:
                Uma mensagem informando o valor da recompensa diária coletada.
        """
        if ctx.channel.id in self.channels:
            today = get_days()
            date = get_daily(ctx.author.id)
            if date < today:
                valor_daily = randint(1000, 3500)
                if get_vip(ctx.author.id):
                    valor_daily += valor_daily
                    daily_embed = discord.Embed(
                        title=" ",
                        description=f"**Você recebeu**: {valor_daily}:drop_of_blood: 2x por ser Vip :star2:",
                        colour=0xFFD301,
                    )
                else:
                    daily_embed = discord.Embed(
                        title=" ",
                        description=f"**Você recebeu**: {valor_daily}:drop_of_blood: ",
                        colour=0xFFD301,
                    )
                add_daily(ctx.author.id, money=valor_daily, daily=today)
                await ctx.send(embed=daily_embed)
            else:
                await ctx.send(f"Você já pegou seu daily hoje.")


def setup(bot):
    """Load Economy Cog."""
    bot.add_cog(Economy(bot))
