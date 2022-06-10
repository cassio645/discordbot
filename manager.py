import discord
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, CommandOnCooldown, BadArgument, MissingPermissions
from discord.ext import tasks
from discord.ext import commands
from discord.utils import get
from db.mydb import delete_data, end_vip, get_all_vip
from code.rank_xp import delete_xp
from code.funcoes import get_days

#from code.asserts import cargos_exclusivos


class Manager(commands.Cog):
    """Manage the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name="k!help", type=3)
        # VERDE Status.online / AMARELO Status.idle/ VERMELHO Status.dnd
        await self.bot.change_presence(status=discord.Status.dnd, activity=activity)
        print(f"{self.bot.user} is alive")
        guild = self.bot.get_guild(565635847508983808)
        role = guild.get_role(977695213457907763)
        channel = self.bot.get_channel(968045281843220520)
        self.manage_vip.start(guild, role, channel)



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
    async def manage_vip(self, guild, role, channel):
        all_vips = get_all_vip()
        today = get_days()
        for vip in all_vips:
            if today >= vip["vip"]:
                end_vip(int(vip["_id"]))
                member = guild.get_member(int(vip["_id"]))
                await member.remove_roles(role)
                #for cargo in cargos_exclusivos:
                 #   cargo_get = get(member.guild.roles, id=cargo)
                  #  await member.remove_roles(cargo_get)
                await channel.send(f'{ctx.author} não é mais vip.')


def setup(bot):
    bot.add_cog(Manager(bot))