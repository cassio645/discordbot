import discord

from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands.errors import MissingPermissions
from EZPaginator import Paginator
from time import sleep
from db.mydb import get_all_vip, insert_vip, remove_money, end_vip, add_capa, get_user_capas, add_cor, get_user_cores
from db.storedb import add_item, get_all_items, get_item, edit_item, remove_item
from .funcoes import pass_to_dict, pass_to_money, get_days, verify_role_or_id, remove_png, get_prefix, find_capa, all_channels, find_cor
from .my_paginate import paginate_store

prefix = get_prefix()


class Store(commands.Cog):
    """Work with Store"""

    def __init__(self, bot):
        self.bot = bot
        self.channels = all_channels()
        
    @commands.command(name="create_item", aliases=["create-item"])
    @commands.has_permissions(administrator=True)          
    async def create_item(self, ctx):
        def check(msg):
            if msg.author == ctx.author:
                return msg.content
        await ctx.send("Criando novo item...")
        await ctx.send('`Qual nome?`')
        response = await self.bot.wait_for("message", check=check, timeout=30)
        name = response.content.lower()
        await ctx.send('`Comando de info/compra` **Não** use a palavra info nem comprar.')
        response = await self.bot.wait_for("message", check=check, timeout=30)
        cmd = response.content.lower()
        await ctx.send('`Descrição` do item.')
        response = await self.bot.wait_for("message", check=check, timeout=30)
        desc = response.content.lower()
        await ctx.send('`Estoque` Use ilimitado ou um número.')
        response = await self.bot.wait_for("message", check=check, timeout=30)
        stock = response.content
        await ctx.send('`Preço` **Não** use ponto nem vírgula.')
        response = await self.bot.wait_for("message", check=check, timeout=30)
        price = response.content

        await ctx.send('`Msg` **MUUITO IMPORTANTE**\nmsg após o usuario realizar a compra **(pq pode-se precisar marcar algum cargo de adm)**.')
        response = await self.bot.wait_for("message", check=check, timeout=30)
        msg = response.content


        await ctx.send("Sim ou Não. Ao comprar o item a pessoa deve receber algum cargo?")
        response = await self.bot.wait_for("message", check=check, timeout=30)

        if response.content.lower().strip()[:1] == 's':
            await ctx.send("Mencione ou envie o ID do cargo que ela deverá receber.")
            response = await self.bot.wait_for("message", check=check, timeout=30)
            role = verify_role_or_id(response.content)
            if not role:
               await ctx.send("Falha no cadastro. Tente novamente.")
               return
            if add_item(name, cmd, desc, stock, price, role, msg):
                await ctx.send("Item adicionado com sucesso.")
            else:
               await ctx.send("Falha no cadastro. Tente novamente.")
               return
        elif add_item(name, cmd, desc, stock, price, msg):
            await ctx.send("Item adicionado com sucesso.")
        else:
            await ctx.send("Falha no cadastro. Tente novamente.")


    @commands.command(name="edit_item", aliases=["edit-item"])
    @commands.has_permissions(administrator=True)
    async def edit_item(self, ctx, *, arg):
        try:
            def check(msg):
                if msg.author == ctx.author:
                    return msg.content
            r = get_item(arg.lower())
            item = f"name: {r['name']}\ncmd: {r['cmd']}\ndesc: {r['desc']}\nstock: {r['stock']}\nprice: {r['price']}\nrole: {r['role']}"
            await ctx.send(item)
            sleep(1)
            await ctx.send("\n**Mande o campo que você quer editar com o novo valor. (1 edit por vez)**\nEx: stock: 3")
            response = await self.bot.wait_for("message", check=check, timeout=30)
            test =''
            for l in response.content:
                if l == ':':
                    break
                test += l
            if test in ["name", "cmd", "desc", "stock", "price", "role"]:
                chave, valor = pass_to_dict(response.content)
                if edit_item(arg, chave, valor):
                    await ctx.send("Alterações salvas com sucesso.")
                else:
                    await ctx.send("Erro ao salvar. Tente novamente.")
                    return
            else:
                await ctx.send("Campo inválido...")
                return
        except:
            await ctx.send("Item não encontrado.")
    
    @commands.command(name="delete_item", aliases=["delete-item", "remove_item", "remove-item"])
    @commands.has_permissions(administrator=True)
    async def delete_item(self, ctx, *, arg):
        try:
            def check(msg):
                if msg.author == ctx.author:
                    return msg.content
            r = get_item(arg.lower())
            item = f"name: {r['name']}\ncmd: {r['cmd']}\ndesc: {r['desc']}\nstock: {r['stock']}\nprice: {r['price']}\nrole: {r['role']}"
            await ctx.send(item)
            sleep(1)
            await ctx.send("\n**Deseja deletar esse item?**\nSim/Não")
            response = await self.bot.wait_for("message", check=check, timeout=30)
            if response.content.strip().lower()[:1] == 's':
                remove_item(arg)
                await ctx.send("Item deletado com sucesso.")
            else:
                await ctx.send("Item NÂO deletado.")
        except:
            await ctx.send("Item não encontrado")


        
    @commands.command()
    async def loja(self, ctx, arg=None):
        if ctx.channel.id in self.channels:
            if arg is None:
                items = get_all_items()
                embed1, embeds = paginate_store(items, len(items), "Completa")
                msg = await ctx.send(embed=embed1)
                page = Paginator(bot=self.bot, message=msg, embeds=embeds)
                await page.start()
            elif arg.lower() in ["capa", "capas"]:
                items = get_all_items("capas")
                embed1, embeds = paginate_store(items, len(items), "de Capas")
                msg = await ctx.send(embed=embed1)
                page = Paginator(bot=self.bot, message=msg, embeds=embeds)
                await page.start()


    @commands.command()
    async def info(self, ctx, *, arg):
        if ctx.channel.id in self.channels:
            if arg:
                item = get_item(arg.lower(), field="cmd")
                if item:
                    name = remove_png(item["name"])
                    price = pass_to_money(item["price"])
                    embed_item = discord.Embed(
                        title=name.title(),
                        description=item["desc"],
                        colour=0xf0c21d
                    )
                    embed_item.add_field(name="Estoque", value=item["stock"])
                    embed_item.add_field(name="Preço", value=f"{price}:drop_of_blood: ")
                    if item["role"]:
                        embed_item.add_field(name="Cargo", value=f'<@&{item["role"]}>')
                    elif item["img"]:
                        embed_item.set_image(url=item["img"])
                    embed_item.add_field(name="Comando para comprar", value=f'`{prefix}comprar {item["cmd"]}`', inline=False)
                    embed_item.set_footer(text='Kivida Bot')
                    await ctx.send(embed=embed_item)
                else:
                    await ctx.send("Item não encontrado")
                    return

    @commands.bot_has_permissions(manage_roles=True)
    @commands.command()
    async def comprar(self, ctx, *, arg):
        if ctx.channel.id in self.channels:
            try:
                item = get_item(arg.lower(), field="cmd")
                if item["stock"] != "ilimitado":
                    if item["stock"] == "0":
                        await ctx.send("Esse produto não possui mais estoque.")
                        return
                    stock = int(item["stock"])
                    item["stock"] = str(stock-1)
                    edit_item(item["name"], "stock", item["stock"])
                
                if item["img"]:
                    capas = get_user_capas(ctx.author.id)
                    possui = item["name"] in capas
                    if not possui:
                        if find_capa(arg.lower()):
                            if remove_money(ctx.author.id, item["price"]):
                                response = add_capa(ctx.author.id, item["cmd"])
                                if response == True:
                                    await ctx.send(f"{item['msg'].capitalize().replace('{prefix}', f'{prefix}')}")
                                    return
                                else:
                                    await ctx.send(response)
                                    return
                            else:
                                await ctx.send("Você não tem kivs suficiente.")
                                return
                        else:
                            await ctx.send(f"Capa não encontrada.")
                            return
                    else:
                        await ctx.send(f"Você já comprou esta capa. Veja em {prefix}capas")
                        return

                elif item["role"] and item["cmd"] not in ["vip 7", "vip 15", "vip 30"]:
                        if remove_money(ctx.author.id, item["price"]):
                            role = discord.utils.get(ctx.guild.roles, id=int(item["role"]))
                            member = ctx.guild.get_member(ctx.author.id)
                            response = add_cor(ctx.author.id, item["cmd"])
                            if response == True:
                                    await ctx.send(f"{item['msg'].capitalize().replace('{prefix}', f'{prefix}')}")
                                    return
                            else:
                                    await ctx.send(response)
                                    return
                        else:
                            await ctx.send("Você não tem kivs suficiente.")
                            return
                elif item["role"] and item["cmd"] in ["vip 7", "vip 15", "vip 30"]:
                    if item["cmd"] == "vip 7":
                        if remove_money(ctx.author.id, item["price"]):
                            role = discord.utils.get(ctx.guild.roles, id=int(item["role"]))
                            member = ctx.guild.get_member(ctx.author.id)
                            insert_vip(ctx.author.id, 7)
                            await member.add_roles(role)
                            await ctx.send(f"{item['msg'].capitalize().replace('{prefix}', f'{prefix}')}")
                        else:
                            await ctx.send("Você não tem kivs suficiente.")
                    elif item["cmd"] == "vip 15":
                        if remove_money(ctx.author.id, item["price"]):
                            role = discord.utils.get(ctx.guild.roles, id=int(item["role"]))
                            member = ctx.guild.get_member(ctx.author.id)
                            insert_vip(ctx.author.id, 15)
                            await member.add_roles(role)
                            await ctx.send(f"{item['msg'].capitalize().replace('{prefix}', f'{prefix}')}")
                        else:
                            await ctx.send("Você não tem kivs suficiente.")
                    elif item["cmd"] == "vip 30":
                        if remove_money(ctx.author.id, item["price"]):
                            role = discord.utils.get(ctx.guild.roles, id=int(item["role"]))
                            member = ctx.guild.get_member(ctx.author.id)
                            insert_vip(ctx.author.id, 30)
                            await member.add_roles(role)
                            await ctx.send(f"{item['msg'].capitalize().replace('{prefix}', f'{prefix}')}")
                        else:
                            await ctx.send("Você não tem kivs suficiente.")
                elif item["cmd"] == "sonhos 10k":
                    if remove_money(ctx.author.id, item["price"]):
                        await ctx.send(f"{item['msg'].capitalize().replace('{prefix}', f'{prefix}')}")
                    else:
                        await ctx.send("Você não tem kivs suficiente.")

            except:
               await ctx.send(f"Não encontrei esse item. Use {prefix}loja")



def setup(bot):
    bot.add_cog(Store(bot))