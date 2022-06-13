import discord
import time
from time import sleep
from random import randint, choices, choice, sample
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from db.mydb import add_money, remove_money
from db.cooldown import add_aposta
from .asserts import dicionario, lista_raspadinha
from .funcoes import get_prefix, pass_to_num

prefix = get_prefix()

def verifica_valor(valor):
    if valor == "<:OWLgg:973214922655821864>":
        return 500
    elif valor == "<:dogecoin:973687932542148608>":
        return 1000
    elif valor == ":x:":
        return 0
    elif valor == "<:alienkiss:973238737867792435>":
        return 10000
    elif valor == "<:bitcoin:973214832499236885>":
        return 30000
    elif valor == "<:rubyheart:973214888539340810>":
        return 1000000
    else:
        return 0

class Casino(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        #pv self.channels = [982321966268686407, 982321436469362778, 982321475996504084, 977271218757570611, 944649962686386256, 883810728140734506]
        self.channels = [944649962686386256, 983462889086124072, 982711181259210833, 968048613806723082, 968045281843220520, 975176426741440542]
    
    # raspadinha
    @commands.command()
    @cooldown(1, 15, BucketType.user)
    async def raspadinha(self, ctx, *, args='.'):
        if((ctx.channel.id) in self.channels):
            if args.lower() == "comprar" or args.lower() == "compra":
                resposta = remove_money(ctx.author.id, 500)
                if resposta:
                    x = randint(0, 2)
                    valor = 0
                    l1 = choices(lista_raspadinha[x], k=3) # linha 1 (k=3 quer dizer que ele vai pegar 3 valores da lista)
                    l2 = sample(lista_raspadinha[x-1], k=3) # linha 2
                    l3 = sample(lista_raspadinha[x-2], k=3) # linha 3 

                    ex_l1 = f"||{l1[0]} {l1[1]} {l1[2]}||"
                    ex_l2 = f"||{l2[0]} {l2[1]} {l2[2]}||"
                    ex_l3 = f"||{l3[0]} {l3[1]} {l3[2]}||"
                    
                    for l in [l1, l2, l3]:          # verificando se ele ganhou em uma linha
                        if l[0] == l[1] == l[2]:
                            valor += verifica_valor(l[0])
                                            
                    for x in range(3):              # verificando se ele ganhou em uma coluna
                        if l1[x] == l2[x] == l3[x]:
                            valor += verifica_valor(l1[x])        
                    
                    if l1[0] == l2[1] == l3[2]:     # verificando se ele ganhou na diagonal
                        valor += verifica_valor(l1[0])
                        
                    if l1[2] == l2[1] == l3[0]:
                        valor += verifica_valor(l1[2])

                    # Exibir para o user
                    if valor > 9999:
                        add_money(ctx.author.id, valor)
                        msg = f"{ctx.author}\n{ex_l1}\n{ex_l2}\n{ex_l3}\n\n||**Prêmio:** {valor}||\n"
                        await ctx.send(msg)
                    elif valor > 999:
                        add_money(ctx.author.id, valor)
                        msg = f"{ctx.author}\n{ex_l1}\n{ex_l2}\n{ex_l3}\n\n||**Prêmio:** {valor}   ||\n"
                        await ctx.send(msg)
                    elif valor > 499:
                        add_money(ctx.author.id, valor)
                        msg = f"{ctx.author}\n{ex_l1}\n{ex_l2}\n{ex_l3}\n\n||**Prêmio:** {valor}     ||\n"
                        await ctx.send(msg)
                    else:
                        msg = f"{ctx.author}\n{ex_l1}\n{ex_l2}\n{ex_l3}\n\n||**Prêmio:** 0          ||\n"
                        await ctx.send(msg)
                else:
                    await ctx.send("Você não tem kivs suficiente.")
            else:
                embed_raspadinha = discord.Embed(
                    title = 'Como comprar uma raspadinha.',
                    description=f'É muito simples você deve usar o comando `{prefix}raspadinha comprar` para obter uma raspadinha. Lembrando que você pode ganhar nas linhas, colunas e diagonais.\n\n**Comando:** `{prefix}raspadinha comprar`ㅤㅤㅤㅤ**Preço:** 500 :drop_of_blood: ',
                    colour=0xFFD301
                )
                embed_raspadinha.add_field(name="Prêmios", value=f"<:OWLgg:973214922655821864> 500:drop_of_blood: \n<:dogecoin:973687932542148608> 1.000:drop_of_blood:  \n<:alienkiss:973238737867792435> 10.000:drop_of_blood: \n<:bitcoin:973214832499236885> 30.000:drop_of_blood: \n<:rubyheart:973214888539340810> 1.000.000:drop_of_blood: ")
                embed_raspadinha.set_footer(text='Kivida Bot')
                await ctx.send(embed=embed_raspadinha)
        else:
            await ctx.send("Esse comando não é permitido aqui nesse canal. <#983462889086124072>")

    @raspadinha.error
    async def raspadinha_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds_input = error.retry_after
            convert = time.strftime("%H:%M:%S", time.gmtime(seconds_input))
            horario = (convert.replace(":", ""))
			# convertendo o tempo que falta para dar 1hr
            await ctx.send(f'Você deve esperar **{convert[-2:]}s** para jogar novamemte.')
   

    # slot-machine
    @commands.command(name="apostar", aliases=["aposta", "cassino"])
    async def apostar(self, ctx, *, arg=0):
        if((ctx.channel.id) in self.channels):
            arg = pass_to_num(arg)
            if (arg is False) or arg <= 0:
                kivs_embed = discord.Embed(title="Apostar", description=f"Aposte para tentar aumentar seus kivs. Você pode apostar qualquer valor, até 5x por hora. Os prêmios serão multiplicações do valor que você apostar. Confira abaixo.\n\n**Modo de usar:** `{prefix}apostar <valor>`\n", colour=0xFFD301)
                kivs_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973589210097385512/banner.png")
                kivs_embed.set_footer(text='Kivida Bot')
                await ctx.send(embed=kivs_embed)
                return
            cd = add_aposta(ctx.author.id)
            if cd == True:
                resposta = remove_money(ctx.author.id, arg)
                if resposta:
                    lista_degif = list(dicionario.keys())
                    numero = randint(1, 1000) # chance de vencer 19%

                    if numero < 4:
                        premio = arg * 60
                        embed_jogo = discord.Embed(title="Jogando caça-niquel", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** -", colour=0xFFD301)
                        embed_jogo.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973322978915917884/bcd07605-7925-4860-8c0e-986af52930b1.gif")
                        embed_jogo.set_footer(text=f"Aposta realizada por {ctx.author}")
                        msg = await ctx.send(embed=embed_jogo)
                        
                        sleep(5)
                        add_money(ctx.author.id, premio)
                        novo_embed = discord.Embed(title="Parabéns você ganhou 60x", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** {premio} :drop_of_blood: ", colour=0x10c727)
                        novo_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973323007881789470/bcd07605.png")
                        novo_embed.set_footer(text=f"Aposta realizada por {ctx.author}")
                        await msg.edit(embed=novo_embed)

                    elif numero < 15:
                        premio = arg * 25
                        embed_jogo = discord.Embed(title="Jogando caça-niquel", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** -", colour=0xFFD301)
                        embed_jogo.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973323461982314496/2c2d65c2-5860-4e1a-be7d-fc44b68c7996.gif")
                        embed_jogo.set_footer(text=f"Aposta realizada por {ctx.author}")
                        msg = await ctx.send(embed=embed_jogo)
                        
                        sleep(5)
                        add_money(ctx.author.id, premio)
                        novo_embed = discord.Embed(title="Parabéns você ganhou 25x", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** {premio} :drop_of_blood: ", colour=0x10c727)
                        novo_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973323504495771678/c2d65c2.png")
                        novo_embed.set_footer(text=f"Aposta realizada por {ctx.author}")
                        await msg.edit(embed=novo_embed)

                    elif numero < 35:
                        premio = arg * 10
                        embed_jogo = discord.Embed(title="Jogando caça-niquel", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** -", colour=0xFFD301)
                        embed_jogo.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973323900811366480/b8b2cf18-e6da-4304-b6b2-c913450218aa.gif")
                        embed_jogo.set_footer(text=f"Aposta realizada por {ctx.author}")
                        msg = await ctx.send(embed=embed_jogo)
                        
                        sleep(5)
                        add_money(ctx.author.id, premio)
                        novo_embed = discord.Embed(title="Parabéns você ganhou 10x", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** {premio} :drop_of_blood: ", colour=0x10c727)
                        novo_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973323934386761858/b8b2cf1.png")
                        novo_embed.set_footer(text=f"Aposta realizada por {ctx.author}")
                        await msg.edit(embed=novo_embed)

                    elif numero < 65:
                        premio = arg * 5
                        embed_jogo = discord.Embed(title="Jogando caça-niquel", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** -", colour=0xFFD301)
                        embed_jogo.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973324296502009876/caaaf766-6b1d-4c96-b2b9-ed58d9c59960.gif")
                        embed_jogo.set_footer(text=f"Aposta realizada por {ctx.author}")
                        msg = await ctx.send(embed=embed_jogo)
                        
                        sleep(5)
                        add_money(ctx.author.id, premio)
                        novo_embed = discord.Embed(title="Parabéns você ganhou 5x", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** {premio} :drop_of_blood: ", colour=0x10c727)
                        novo_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973324319537123398/caaaf766.png")
                        novo_embed.set_footer(text=f"Aposta realizada por {ctx.author}")
                        await msg.edit(embed=novo_embed)

                    elif numero < 120:
                        premio = arg * 2
                        embed_jogo = discord.Embed(title="Jogando caça-niquel", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** -", colour=0xFFD301)
                        embed_jogo.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973324650165706773/e10fe8b4-99ea-49df-9bc0-7f312cd36313.gif")
                        embed_jogo.set_footer(text=f"Aposta realizada por {ctx.author}")
                        msg = await ctx.send(embed=embed_jogo)
                        
                        sleep(5)
                        add_money(ctx.author.id, premio)
                        novo_embed = discord.Embed(title="Parabéns você ganhou 2x", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** {premio} :drop_of_blood: ", colour=0x10c727)
                        novo_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973324677407703140/e10fe8b4.png")
                        novo_embed.set_footer(text=f"Aposta realizada por {ctx.author}")
                        await msg.edit(embed=novo_embed)

                    else:
                        # vai pegar um dos gifs que não ganha
                        escolha = choice(lista_degif)
                        embed_jogo = discord.Embed(title="Jogando caça-niquel", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** -", colour=0xFFD301)
                        embed_jogo.set_image(url=escolha)
                        embed_jogo.set_footer(text=f"Aposta realizada por {ctx.author}")
                        msg = await ctx.send(embed=embed_jogo)
                        img = dicionario[escolha]
                        sleep(5)
                        novo_embed = discord.Embed(title="Que pena...", description=f"**Valor apostado:** {arg} :drop_of_blood: \n**Prêmio:** 0", colour=0xc71010)
                        novo_embed.set_image(url=img)
                        novo_embed.set_footer(text=f"Aposta realizada por {ctx.author}")
                        await msg.edit(embed=novo_embed)
                else:
                    await ctx.send("Você não tem kivs suficiente.")
            else:
                await ctx.send(f"Você precisa esperar mais {cd[:2]}m {cd[3:]}s")
        else:
            await ctx.send("Esse comando não é permitido aqui. <#983462889086124072>")


	
def setup(bot):
    """Load Casino Cog."""
    bot.add_cog(Casino(bot))