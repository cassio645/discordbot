import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from .funcoes import get_prefix

prefix = get_prefix()


class HelpCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# Help console

	@commands.command()
	@cooldown(1, 3, BucketType.channel)
	async def help(self, ctx, argument=None, page = None):

		# Help comandos
		comandos_embed = discord.Embed(
				title = 'Comandos do Kivida Bot',
				description=f'**ping**\nTempo de resposta do bot.\n**Modo de usar:** `{prefix}ping`\n\n'
							f'**avatar** | **av**\nMostra seu avatar ou do usuário mencionado\n**Modo de usar:** `{prefix}avatar <@membro | ID>`\n\n'
							f'**userinfo | ui**\nMostra informações do usuário\n**Modo de usar:** `{prefix}userinfo <@membro | ID>`\n\n'
							f'**serverinfo | si**\nMostra informações do servidor\n**Modo de usar:** `{prefix}serverinfo`\n\n'
							f'**encurta | diminui**\nUse esse comando para deixar um link muito grande menor.\n**Modo de usar:** `{prefix}encurta <link>`\n\n'
							f'**calcular | calc**\nCalcula expressões matematicas\n**Modo de usar:** `{prefix}calc (1+1)*3`\n\n',
				colour=0xFFD301
			)
		comandos_embed.set_footer(text='Kivida Bot')

		# Embed Perfil
		perfil_embed = discord.Embed(
			title = "Perfil Kivida Bot",
			description=f'**perfil**\nMostra seu perfil com suas informações\n**Modo de usar:** `{prefix}perfil` | `{prefix}perfil <@membro | ID>`\n\n'
						f'**status**\nAltera o status do seu perfil.\n**Modo de usar:** `{prefix}status <frase>`\n\n'
						f'**capas**\nVeja as capas que você comprou na loja.\n**Modo de usar:** `{prefix}capas`\n\n'
						f'**usar**\nAltera a capa do seu perfil.\n**Modo de usar:** `{prefix}usar <capa>`\n\n'
						f'**rep**\nEnvie uma reputação a um usuário\n**Modo de usar:** `{prefix}rep <@membro | ID>`\n\n'
						f'**rank reps**\nVeja a lista das pessoas que mais receberam reps\n**Modo de usar:** `{prefix}rank reps`\n\n'
						f'**rank xp**\nVeja as pessoas mais ativas do servidor\n**Modo de usar:** `{prefix}rank xp`\n\n',
						colour=0xFFD301
					)
		perfil_embed.set_footer(text='Kivida Bot')

		# Embed Loja
		loja_embed = discord.Embed(
			title= "Loja do Kivida",
			description=f"**loja**\nUma otima maneira de gastar seus diamantes, com capas, cargos (LOJA COMPLETA).\n**Modo de usar:** `{prefix}loja`\n\n"
			f"**loja capas**\nMostra apenas as capas(backgrounds), que você pode comprar para seu perfil.\n**Modo de usar:** `{prefix}loja capas`\n\n"
			f"**info**\nVeja as informações de um item da loja, como preço, estoque e o comando de compra do item\n**Modo de usar:** `{prefix}info <name>`\n\n"
			f"**comprar**\nCompre um item da loja com esse comando.\n**Modo de usar:** `{prefix}comprar <name>`\n\n",
			colour=0xFFD301
		)
		loja_embed.set_footer(text='Kivida Bot')

		# Embed Games
		games_embed = discord.Embed(
				title = 'Games do Kivida Bot',
				description=f'**adivinhar | adv**\n O bot pensará em um número entre 1 e 100. e se você acertar o número em 4 tentativas, 5.000<:diamantt:973404655050719232>\n**Modo de usar:** `{prefix}adivinhar`'
				f'**rank c4**\n Veja o rank de vitórias do jogo Connect4\n(Jogos contra o bot não contam vitória.)\n**Modo de usar:** `{prefix}rank c4`',
				colour=0xFFD301
			)
		games_embed.add_field(name="CONNECT 4", value=f'**connect4** | **c4**\nJogue connect4 contra outro usuário ou contra o bot\n**Modo de usar:** `{prefix}c4 | {prefix}c4 bot`\n\n', inline=False)
		games_embed.set_image(url="https://cdn.discordapp.com/attachments/858056671759040522/962683801383890984/connect4.png")
		games_embed.set_footer(text='Kivida Bot')

		# Embed diamantes
		diamantes_embed = discord.Embed(
			title = 'Diamantes Kivida Bot',
			description =f"**diamantes | money**\n Com esse comando você pode consultar quantos diamantes <:diamantt:973404655050719232> você tem.\n**Modo de usar:** `{prefix}diamantes`\n\n"
			f"**daily**\n Pegue diariamente uma quantia em diamantes com esse comando.\n**Modo de usar:** `{prefix}daily`\n\n"
			f"**rank diamantes**\n Vejo o rank dos mais ricos com esse comando\n**Modo de usar:** `{prefix}rank diamantes`\n\n"
			f"**raspadinha**\n Compre uma raspadinha e para tentar aumentar seus diamantes, cada uma delas custa 500 <:diamantt:973404655050719232>, você pode ganhar nas linhas, colunas e diagonais.\n**Modo de usar:** `{prefix}raspadinha comprar`\n\n",
			colour=0xFFD301
			)
		diamantes_embed.add_field(name="\nㅤㅤㅤㅤㅤㅤㅤㅤCassino\n", value=f"**apostar**\nVocê pode tentar aumentar seus diamantes apostando nas máquinas.\nLembrando que você pode jogar até 5 vezes a cada hora.\n\n**Modo de usar:** `{prefix}apostar <valor>`\n\n")
		diamantes_embed.set_image(url="https://cdn.discordapp.com/attachments/883810728140734506/973589210097385512/banner.png")
		diamantes_embed.set_footer(text='Kivida Bot')
		
		# Embed inicial
		initial_help_dialogue = discord.Embed(
				title = 'Comandos Help Kivida',
				description=f'`{prefix}help comandos`\nComandos em geral\n\n'
							f'`{prefix}help perfil`\nComandos do seu perfil\n\n'
							f'`{prefix}help loja`\nComandos da loja\n\n'
							f"`{prefix}help diamantes`\nComandos de economia e cassino\n\n"
							f'`{prefix}help games`\nComandos dos Games\n\n',
				colour=0xFFD301
				)
		initial_help_dialogue.set_thumbnail(
				url=
				'https://cdn.discordapp.com/attachments/979065286705700955/981573706239320074/3_Sem_Ttulo_20220531225244.png'
				)
		initial_help_dialogue.set_image(
					url=
					'https://cdn.discordapp.com/attachments/979065286705700955/981576391822815232/Photo_1654095758656.png'
				)		
		initial_help_dialogue.set_footer(text='Criado por: @CASSIO645#3477')

		if argument is None:
			await ctx.send(embed=initial_help_dialogue)
		elif argument.lower() == 'comandos':
			await ctx.send(embed=comandos_embed)
		elif argument.lower() == 'diamante' or argument.lower() == 'diamantes' or argument.lower() == 'apostar':
			await ctx.send(embed=diamantes_embed)
		elif argument.lower() == 'games' or argument.lower() == 'game':
			await ctx.send(embed=games_embed)
		elif argument.lower() == 'perfil':
			await ctx.send(embed=perfil_embed)
		elif argument.lower() == "loja":
			await ctx.send(embed=loja_embed)
		else:
		  pass



def setup(bot):
	bot.add_cog(HelpCog(bot))