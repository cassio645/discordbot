import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, CommandOnCooldown, BadArgument, MissingPermissions
from discord.ext import tasks
from discord.ext import commands
from discord.utils import get
from db.mydb import delete_data, end_vip, get_all_vip
from code.rank_xp import delete_xp
from code.funcoes import get_days

from code.asserts import lista_de_cores


class Manager(commands.Cog):
    """Manage the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name="!help", type=3)
        # VERDE Status.online / AMARELO Status.idle/ VERMELHO Status.dnd
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        print(f"{self.bot.user} is alive")
        guild = self.bot.get_guild(940739788871467049)
        role = guild.get_role(977933606259425290)
        self.manage_vip.start(guild, role)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            pass
        elif isinstance(error, CommandNotFound):
            pass
        elif isinstance(error, CommandOnCooldown):
            pass
        elif isinstance(error, BadArgument):
            pass
        elif isinstance(error, MissingPermissions):
            await ctx.send("Você não tem permissão para usar este comando.")
        else:
            raise error

        # Apaga os dados dos usuários que sairam do servidor
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        delete_data(member.id)
        delete_xp(member.id)

    def cog_unload(self):
        self.manage_vip.cancel()

    @tasks.loop(hours=12)
    async def manage_vip(self, guild, role):
        all_vips = get_all_vip()
        today = get_days()
        for vip in all_vips:
            if today >= vip["vip"]:
                end_vip(int(vip["_id"]))
                member = guild.get_member(int(vip["_id"]))
                await member.remove_roles(role)
                for cor in lista_de_cores:
                    cor_get = get(member.guild.roles, id=cor)
                    await member.remove_roles(cor_get)


def setup(bot):
    bot.add_cog(Manager(bot))