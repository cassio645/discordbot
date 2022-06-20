import discord
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from .funcoes import get_prefix, find_capa, find_cor, get_id, all_channels
from db.eventdb import get_milho, remove_milho, add_categoria, add_milho
#from db.premiodb import get_premio, edit_premio, get_embed_premios
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
        #self.channels = [985991485876998207, 985989056502562886, 985962497364328499]
        self.channels = all_channels()

    @commands.command(name="milho", aliases=["milhos", "evento"])
    async def milho(self, ctx):
        if((ctx.channel.id) in self.channels):
            milhos = get_milho(ctx.author.id)
            if milhos:
                embed_milho = discord.Embed(title="  ", description=f"**Você possui {milhos['milho']} :corn:**", colour=0xFFD301)
                await ctx.send(embed=embed_milho)
            else:
                embed_milho = discord.Embed(title="  ", description=f"**Você possui 0 :corn:**", colour=0xFFD301)
                await ctx.send(embed=embed_milho)



    @commands.command(name="enviar_milho", aliases=["enviar-milho"])
    @commands.has_permissions(administrator=True)
    async def enviar_milho(self, ctx, user=None, milho=None):
        if ctx.channel.id in self.channels:
            try:
                if user and milho:
                    if len(user) < 18 and len(milho) >= 18:
                        user, milho = milho, user
                        
                    user = get_id(user)
                    milho = int(milho)
                    if user and milho:
                        add_milho(user, milho)
                        await ctx.send("Pagamento feito.")
                    else:
                        await ctx.send("Algo deu errado.")
                        return
                elif user and not milho:
                    await ctx.send("Você não informou o valor.")
                    return
                elif milho and not user:
                    await ctx.send("Você não informou o usuário.")
                    return
                else:
                    await ctx.send(f"`{prefix}enviar-milho <@membro | ID> <valor>`")
                    return
            except:
                await ctx.send("Algo deu errado.")


'''
    @commands.command()
    async def first(self, ctx):
        self.manage_premios.start(ctx=ctx, num=1)

    @commands.command()
    async def premios(self, ctx, *, arg:int):
        desc = ''
        if arg == 1:
            response = get_embed_premios(1)
            for x in response:
                desc += f"**Prêmio:** {x['name'].capitalize()}\n**Descrição:** {x['desc'].capitalize()}\n**Valor:** {x['price']}:corn:ㅤㅤㅤㅤ**Estoque:** {x['stock']}\n**Use:** `k!resgatar {x['name']}`\n\n"
            embed_premios = discord.Embed(title="Premios", description=desc, colour=0x009900)
        elif arg == 2:
            embed_premios = discord.Embed(title="Premios Capas 15.000", description="Qualquer capa abaixo custa 5:corn:\n**Você pode resgatar apenas uma dessa categoria.**\n\n**Use**: `k!resgatar capa <nome>`\n\n", colour=0x009900)
            embed_premios.set_image(url="https://cdn.discordapp.com/attachments/979065286705700955/987008772574703696/capa5.jpg")
        elif arg == 3:
            embed_premios = discord.Embed(title="Premios Capas 10.000", description="Qualquer capa abaixo custa 5:corn:\n**Você pode resgatar apenas uma dessa categoria.**\n\n**Use**: `k!resgatar capa <nome>`\n\n", colour=0x009900)
            embed_premios.set_image(url="https://cdn.discordapp.com/attachments/979065286705700955/987008795483992104/capa6.jpg")
        elif arg == 4:
            embed_premios = discord.Embed(title="Premios Capas 8.000", description="Qualquer capa abaixo custa 5:corn:\n**Você pode resgatar apenas uma dessa categoria.**\n\n**Use**: `k!resgatar capa <nome>`\n\n", colour=0x009900)
            embed_premios.set_image(url="https://cdn.discordapp.com/attachments/979065286705700955/986996770552823888/capa7.jpg")
        elif arg == 5:
            embed_premios = discord.Embed(title="Premios Cores 15.000", description="Qualquer cor abaixo custa 5:corn:\n**Você pode resgatar apenas uma dessa categoria.**\n\n**Use:** `k!resgatar cor <nome>`\n**NÃO** precisa do @\n\n", colour=0x009900)
            embed_premios.add_field(name="Cores:", value="<@&971846285520953355> <@&977932632065208370> <@&977932639912742922>\n<@&986627944489316392> <@&986627949291786280> <@&986627952248770560>")
        elif arg == 6:
            embed_premios = discord.Embed(title="Premios Cores 10.000", description="Qualquer cor abaixo custa 5:corn:\n**Você pode resgatar apenas uma dessa categoria.**\n\n**Use:** `k!resgatar cor <nome>`\n**NÃO** precisa do @\n\n", colour=0x009900)
            embed_premios.add_field(name="Cores:", value="<@&977930708188286986> <@&986627950130626680>\n<@&986627950738804826><@&977930579494469732> <@&986627951648989244>")
        elif arg == 7:
            embed_premios = discord.Embed(title="Premios Cores 5.000", description="Qualquer cor abaixo custa 5:corn:\n**Você pode resgatar apenas uma dessa categoria.**\n\n**Use:** `k!resgatar cor <nome>`\n**NÃO** precisa do @\n\n", colour=0x009900)
            embed_premios.add_field(name="Cores:", value="<@&986627953121193984> <@&986627954572419082> <@&986627953880338432>")
        await ctx.send(embed=embed_premios)


    def cog_unload(self):
        self.manage_premios.cancel()

    @tasks.loop(seconds=15)
    async def manage_premios(self, ctx, num=0):
        response = get_embed_premios(1)
        desc = ''
        for x in response:
            desc += f"**Prêmio:** {x['name'].capitalize()}\n**Descrição:** {x['desc'].capitalize()}\n**Valor:** {x['price']}:corn:ㅤㅤㅤㅤ**Estoque:** {x['stock']}\n**Use:** `k!resgatar{x['name']}`\n\n"
        embed_premios = discord.Embed(title="Premios", description=desc, colour=0x009900)
        channel = self.bot.get_channel(986979322650824714)
        msg = await channel.send(embed=embed_premios)
        if num == 1:
            response = get_embed_premios(1)
            for x in response:
                desc += f"**Prêmio:** {x['name'].capitalize()}\n**Descrição:** {x['desc'].capitalize()}\n**Valor:** {x['price']}:corn:ㅤㅤㅤㅤ**Estoque:** {x['stock']}\n**Use:** `k!resgatar{x['name']}`\n\n"
            novo_embed = discord.Embed(title="Premios", description=desc, colour=0x009900)
            channel = self.bot.get_channel(986979322650824714)
            await msg.edit(embed=novo_embed)
'''

def setup(bot):
    """Load Evento Cog."""
    bot.add_cog(Evento(bot))

'''
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
                            if item["categoria"] in [3, 8, 9, 10]:
                                if 8 in resgatados["premios"] and item["categoria"] == 8:
                                    await ctx.send("Você já resgatou um item desta categoria.")
                                    return
                                elif 9 in resgatados["premios"] and item["categoria"] == 9:
                                    await ctx.send("Você já resgatou um item desta categoria.")
                                    return
                                elif 10 in resgatados["premios"] and item["categoria"] == 10:
                                    await ctx.send("Você já resgatou um item desta categoria.")
                                    return
                                elif 3 in resgatados["premios"] and item["categoria"] == 3:
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
'''