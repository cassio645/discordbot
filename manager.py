import discord
from discord.ext.commands.errors import (
    CommandNotFound,
    MissingRequiredArgument,
    CommandOnCooldown,
    BadArgument,
    MissingPermissions,
)
from discord.ext import commands
from db.mydb import delete_data
from code.rank_xp import delete_xp


class Manager(commands.Cog):
    """
    Uma classe de gerenciamento para o bot Discord.

    Esta classe gerencia eventos relacionados ao bot e fornece funções úteis de gerenciamento.
    """

    SERVER_ID = ""
    VIP_ID = ""

    def __init__(self, bot):
        """
        Inicializa uma instância de Manager.

        Args:
            bot (commands.Bot): O bot Discord ao qual esta classe está associada.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Define o status e a atividade do bot quando ele se conecta.
        """
        activity = discord.Game(name="k!help", type=3)
        # VERDE Status.online / AMARELO Status.idle/ VERMELHO Status.dnd
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        print(f"{self.bot.user} is alive")
        # guild = self.bot.get_guild(int(SERVER_ID))
        # role = guild.get_role(int(VIP_ID))
        # self.manage_vip.start(guild, role)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Gerencia erros específicos do comando e fornece uma resposta personalizada.

        Args:
            ctx (commands.Context): O contexto do comando que causou o erro.
            error (Exception): O erro que ocorreu.
        """
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
    async def on_member_remove(self, member: int):
        """
        Executa a exclusão de dados relacionados a um membro que saiu do servidor.

        Args:
            member (discord.Member): O membro que saiu do servidor.
        """
        delete_data(member.id)
        delete_xp(member.id)


"""
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
"""


def setup(bot):
    bot.add_cog(Manager(bot))
