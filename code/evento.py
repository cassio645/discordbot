import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from .funcoes import get_prefix, find_capa, find_cor
from db.eventdb import get_milho, remove_milho, add_categoria
from db.premiodb import get_premio, edit_premio
from db.mydb import get_user_capas, get_user_cores, add_capa, add_cor, insert_vip



prefix = get_prefix()


def check_stock(item):
    if item["stock"] <= 0:
        return "Esse produto não possui mais estoque."
    item["stock"] -= 1
    edit_premio(item["name"], "stock", item["stock"])
    return True

class Evento(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channels = [985991485876998207, 985989056502562886, 985962497364328499]
        #self.channels = [944649962686386256, 983462889086124072, 982711181259210833, 968048613806723082, 968045281843220520, 975176426741440542]


    @commands.command(name="milho", aliases=["milhos", "evento"])
    async def milho(self, ctx):
        milhos = get_milho(ctx.author.id)
        embed_milho = discord.Embed(title="  ", description=f"**Você possui {milhos['milho']} :corn:**", colour=0xFFD301)
        await ctx.send(embed=embed_milho)

    @commands.command()
    async def resgatar(self, ctx, *, arg):
         if ctx.channel.id in self.channels:
                if "capa" in arg.lower():
                    arg = arg.lower() + ".png"
                item = get_premio(arg.lower())
                resgatados = get_milho(ctx.author.id)
                if item == False:
                    await ctx.send("Não encontrei esse item. Use\n`k!resgatar <categoria> <nome>`")
                    return
                if item["categoria"] in [5, 6, 7]:
                    if 5 in resgatados["premios"] and item["categoria"] == 5:
                        await ctx.send("Você já resgatou um item desta categoria.")
                        return
                    elif 6 in resgatados["premios"] and item["categoria"] == 6:
                        await ctx.send("Você já resgatou um item desta categoria.")
                        return
                    elif 7 in resgatados["premios"] and item["categoria"] == 7:
                        await ctx.send("Você já resgatou um item desta categoria.")
                        return
                    response = check_stock(item)
                    if response != True:
                        await ctx.send(response)
                        return
                    capas = get_user_capas(ctx.author.id)
                    nome_da_capa = item["name"].replace("capa", "")
                    nome_da_capa = nome_da_capa.replace(".png", "").strip()
                    possui = nome_da_capa in capas
                    if not possui:
                        capa = find_capa(nome_da_capa)
                        if capa:
                            if remove_milho(ctx.author.id, item["price"]):# remove milho
                                response = add_capa(ctx.author.id, nome_da_capa)
                                if response == True:
                                    await ctx.send(f"{item['msg']}")
                                    add_categoria(ctx.author.id, item["categoria"])
                                    return
                                else:
                                    await ctx.send(response)
                                    return
                            else:
                                await ctx.send("Você não tem milhos suficiente.")
                                return
                        else:
                            await ctx.send(f"Capa não encontrada.")
                            return
                    else:
                        await ctx.send(f"Você já comprou esta capa. Veja em {prefix}capas")
                        return

                elif item["role"] and item["name"] not in ["vip"]:
                        cores = get_user_cores(ctx.author.id)
                        nome_da_cor = item["name"].replace("Cor", "")
                        possui = item["role"] in cores
                        if not possui:
                            if item["categoria"] in [8, 9, 10]:
                                if 8 in resgatados["premios"] and item["categoria"] == 8:
                                    await ctx.send("Você já resgatou um item desta categoria.")
                                    return
                                elif 9 in resgatados["premios"] and item["categoria"] == 9:
                                    await ctx.send("Você já resgatou um item desta categoria.")
                                    return
                                elif 10 in resgatados["premios"] and item["categoria"] == 10:
                                    await ctx.send("Você já resgatou um item desta categoria.")
                                    return
                                response = check_stock(item)
                                if response != True:
                                    await ctx.send(response)
                                    return
                            if remove_milho(ctx.author.id, item["price"]): # remove milho
                                role = discord.utils.get(ctx.guild.roles, id=int(item["role"]))
                                member = ctx.guild.get_member(ctx.author.id)
                                response = add_cor(ctx.author.id, nome_da_cor)
                                if response == True:
                                        await ctx.send(f"{item['msg']}")
                                        add_categoria(ctx.author.id, item["categoria"])
                                        return
                                else:
                                        await ctx.send(response)
                                        return
                            else:
                                await ctx.send("Você não tem milhos suficiente.")
                                return
                        else:
                            await ctx.send(f"Você já tem essa cor. Veja em {prefix}cores")
                            return
                elif item["role"] and item["name"] in ["vip", "cargo vip"]:
                    if 1 in resgatados["premios"] and item["categoria"] == 1:
                        await ctx.send("Você já resgatou esse item.")
                        return
                    response = check_stock(item)
                    if response != True:
                        await ctx.send(response)
                        return
                    if remove_milho(ctx.author.id, item["price"]): # remove milhos
                        role = discord.utils.get(ctx.guild.roles, id=int(item["role"]))
                        member = ctx.guild.get_member(ctx.author.id)
                        insert_vip(ctx.author.id, 30)
                        await member.add_roles(role)
                        await ctx.send(f"{item['msg']}")
                        add_categoria(ctx.author.id, item["categoria"])
                        #channel = self.bot.get_channel(968045281843220520)
                        #await channel.send(f'{ctx.author} se tornou vip.')
                    else:
                        await ctx.send("Você não tem milhos suficiente.")
                elif item["name"] == "sonhos":
                    if 2 in resgatados["premios"] and item["categoria"] == 2:
                        await ctx.send("Você já resgatou esse item.")
                        return
                    response = check_stock(item)
                    if response != True:
                        await ctx.send(response)
                        return
                    if remove_milho(ctx.author.id, item["price"]): # remove milhos
                        await ctx.send(f"{item['msg']}")
                        add_categoria(ctx.author.id, item["categoria"])
                    else:
                        await ctx.send("Você não tem milhos suficiente.")




def setup(bot):
    """Load Evento Cog."""
    bot.add_cog(Evento(bot))
