import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from .funcoes import get_prefix
from db.eventdb import get_milho

prefix = get_prefix()


class Evento(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channels = [982321966268686407, 982321436469362778, 982321475996504084, 977271218757570611, 944649962686386256, 883810728140734506]
        #self.channels = [944649962686386256, 983462889086124072, 982711181259210833, 968048613806723082, 968045281843220520, 975176426741440542]


    @commands.command(name="milho", aliases=["milhos", "evento"])
    async def milho(self, ctx):
        milhos = get_milho(ctx.author.id)
        embed_milho = discord.Embed(title="  ", description=f"**Você possui {milhos} :corn:**", colour=0xFFD301)
        await ctx.send(embed=embed_milho)


def setup(bot):
    """Load Evento Cog."""
    bot.add_cog(Evento(bot))
