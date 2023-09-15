import discord
import pyshorteners
from EZPaginator import Paginator
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import MemberConverter

from .funcoes import get_prefix, all_channels, get_days
from .rank_xp import get_xp_rank
from .my_paginate import paginate_rank

from db.mydb import get_rank, get_daily, get_time_rep
from db.cooldown import get_cooldown_aposta, get_cooldown_guess

from db.eventdb import get_all_milho


prefix = get_prefix()


class GeneralCog(commands.Cog):
    """
    Uma classe de extensão do módulo commands.Cog que fornece comandos gerais e úteis.
    """

    def __init__(self, bot):
        """
        Inicializa a classe GeneralCog.

        Parâmetros:
        bot (discord.ext.commands.Bot): O bot Discord.
        """
        self.bot = bot
        self.channels = all_channels()

    # ping
    @commands.command()
    async def ping(self, ctx) -> None:
        """Retorna a velocidade de resposta do bot em milissegundos."""
        if ctx.channel.id in self.channels:
            "Velocidade de resposta do bot."
            await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    # Avatar fetcher
    @commands.command(aliases=["av"])
    @cooldown(1, 5, BucketType.channel)
    async def avatar(self, ctx, member: discord.Member, override=None) -> None:
        """
        Mostra o avatar de um membro especificado ou do autor da mensagem.

        Parâmetros:
        - `member`: Menção, ID ou nome do membro cujo avatar deseja visualizar. (opcional)
        - `override`: Ignorado, não é utilizado no comando. (opcional)
        """
        if ctx.channel.id in self.channels:
            if member[0] == "<" and member[1] == "@":
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
                member = int(member)
            else:
                pass

            members = await ctx.guild.fetch_members().flatten()
            multiple_member_array = []

            if isinstance(member, discord.Member):
                for members_list in members:
                    if member.name.lower() in members_list.name.lower():
                        multiple_member_array.append(members_list)
                    else:
                        pass
            elif isinstance(member, int):
                for member_list in members:
                    if member_list.id == member:
                        multiple_member_array.append(member_list)
                    else:
                        pass
            else:
                for members_list in members:
                    if member.lower() in members_list.name.lower():
                        multiple_member_array.append(members_list)
                    else:
                        pass

            if member is discord.Member:
                if (
                    member.isdigit()
                    and member.lower() == "me"
                    and override == "override"
                ):
                    embed = discord.Embed(colour=0xFFD301)
                    embed.set_image(url=f"{ctx.author.avatar_url}")
                    await ctx.send(embed=embed)

            elif len(multiple_member_array) == 1:
                if (
                    multiple_member_array[0].name
                    == multiple_member_array[0].display_name
                ):
                    embed = discord.Embed(
                        title=f"{multiple_member_array[0]}", colour=0xFFD301
                    )

                elif (
                    multiple_member_array[0].name
                    != multiple_member_array[0].display_name
                ):
                    embed = discord.Embed(
                        title=f"{multiple_member_array[0]}({multiple_member_array[0].display_name})",
                        colour=0xFFD301,
                    )

                embed.set_image(url=f"{multiple_member_array[0].avatar_url}")
                await ctx.send(embed=embed)

            elif len(multiple_member_array) > 1:
                multiple_member_array_duplicate_array = []
                for multiple_member_array_duplicate in multiple_member_array:
                    if len(multiple_member_array_duplicate_array) < 10:
                        multiple_member_array_duplicate_array.append(
                            multiple_member_array_duplicate.name
                        )
                    else:
                        break

                embed = discord.Embed(
                    title=f"Procurando por {member}\nEncontramos alguns resultados (Max 10)",
                    description=f"\n".join(multiple_member_array_duplicate_array),
                    colour=0x808080,
                )
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"O membro `{member}` não foi encontrado!")

    # Userinfo
    @commands.command(aliases=["ui"])
    @cooldown(1, 5, BucketType.channel)
    async def userinfo(self, ctx, member: discord.Member) -> None:
        """
        Mostra informações detalhadas de um membro especificado no servidor.

        Parâmetros:
        - `member`: Menção, ID ou nome do membro cujas informações deseja visualizar.
        """
        if ctx.channel.id in self.channels:
            if member[0] == "<" and member[1] == "@":
                converter = MemberConverter()
                member = await converter.convert(ctx, member)
            elif member.isdigit():
                member = int(member)

            members = await ctx.guild.fetch_members().flatten()
            multiple_member_array = []

            if isinstance(member, discord.Member):
                for members_list in members:
                    if member.name.lower() in members_list.name.lower():
                        multiple_member_array.append(members_list)
                    else:
                        pass

            elif isinstance(member, int):
                for member_list in members:
                    if member_list.id == member:
                        multiple_member_array.append(member_list)
                    else:
                        pass

            else:
                for members_list in members:
                    if member.lower() in members_list.name.lower():
                        multiple_member_array.append(members_list)
                    else:
                        pass

            if len(multiple_member_array) == 1:
                roles = []
                for role in multiple_member_array[0].roles:
                    roles.append(role)

                embed = discord.Embed(
                    colour=0xFFD301,
                )
                embed.set_author(name=f"User Info - {multiple_member_array[0]}")
                embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
                embed.set_footer(text="Kivida Bot")

                embed.add_field(name="ID:", value=multiple_member_array[0].id)
                embed.add_field(name="Nome:", value=multiple_member_array[0])
                embed.add_field(
                    name="Nickname:", value=multiple_member_array[0].display_name
                )

                embed.add_field(
                    name="Criado: ",
                    value=multiple_member_array[0].created_at.strftime("%#d/%m/%Y"),
                )
                embed.add_field(
                    name="Entrou:",
                    value=multiple_member_array[0].joined_at.strftime("%#d/%m/%Y"),
                )

                if len(roles) == 1:
                    embed.add_field(
                        name=f"Roles ({len(roles) - 1})", value="**Nenhum**"
                    )
                else:
                    embed.add_field(
                        name=f"Roles ({len(roles) - 1})",
                        value=" ".join(
                            [role.mention for role in roles if role.name != "@everyone"]
                        ),
                    )

                embed.add_field(name="Bot?", value=multiple_member_array[0].bot)

                await ctx.send(embed=embed)

            elif len(multiple_member_array) > 1:
                multiple_member_array_duplicate_array = []
                for multiple_member_array_duplicate in multiple_member_array:
                    if len(multiple_member_array_duplicate_array) < 10:
                        multiple_member_array_duplicate_array.append(
                            multiple_member_array_duplicate.name
                        )
                    else:
                        break

                embed = discord.Embed(
                    title=f"Procurando por {member}\nEncontramos alguns resultados (Max 10)",
                    description=f"\n".join(multiple_member_array_duplicate_array),
                    colour=0xFFD301,
                )
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"O membro `{member}` não foi encontrado!")

    # Encurta links
    @commands.command(name="encurta", aliases=["diminui"])
    async def encurta(self, ctx, link: str) -> None:
        """
        Encurta um link fornecido pelo usuário.

        Parâmetros:
        - `link`: O link que você deseja encurtar.
        """
        s = pyshorteners.Shortener()
        await ctx.send(f"`{s.clckru.short(str(link))}`")

    # Calcula
    @commands.command(name="calcular", aliases=["calc"])
    async def calculate_expression(self, ctx, *expression: str) -> None:
        """
        Calcula uma expressão matemática.

        Parâmetros:
        - `expression`: A expressão matemática a ser calculada.
        """
        if ctx.channel.id in self.channels:
            expression = "".join(expression)
            try:
                response = eval(expression)
                await ctx.send("A resposta é: " + str(response))
            except:
                await ctx.send(f"`{expression}` A expressão é invalida!")

    # Server info
    @commands.command(aliases=["si"])
    @cooldown(1, 4, BucketType.channel)
    async def serverinfo(self, ctx) -> None:
        """
        Retorna informações sobre o servidor.

        Parâmetros:
        ctx (commands.Context): O contexto da mensagem.
        """
        if ctx.channel.id in self.channels:
            count = 0

            members = await ctx.guild.fetch_members().flatten()

            for people in members:
                if people.bot:
                    count = count + 1
            else:
                pass

            embed = discord.Embed(title=f"{ctx.guild.name} info", colour=0xFFD301)
            embed.set_thumbnail(url=ctx.guild.icon_url)

            embed.add_field(name="Dono:", value=f"<@{ctx.guild.owner_id}>")
            embed.add_field(name="Id do Servidor:", value=ctx.guild.id)

            embed.add_field(name="País do Servidor:", value="Brasil")
            embed.add_field(name="Membros:", value=ctx.guild.member_count)
            embed.add_field(name="bots:", value=count)
            embed.add_field(name="Pessoas:", value=ctx.guild.member_count - count)

            embed.add_field(name="Numero de cargos:", value=len(ctx.guild.roles))
            embed.add_field(
                name="Numero de bots:", value=ctx.guild.premium_subscription_count
            )

            embed.add_field(name="Canais de Texto:", value=len(ctx.guild.text_channels))
            embed.add_field(name="Canais de Voz:", value=len(ctx.guild.voice_channels))
            embed.add_field(name="Categorias:", value=len(ctx.guild.categories))

            embed.add_field(
                name="Criado em:", value=ctx.guild.created_at.strftime("%#d/%m/%Y")
            )

            await ctx.send(embed=embed)

    @commands.command()
    async def rank(self, ctx, *, arg: str = ".") -> None:
        """
        Mostra o ranking de diferentes estatísticas.

        Parâmetros:
        ctx (commands.Context): O contexto da mensagem.
        arg (str): O argumento que especifica qual ranking mostrar. Pode ser "diamante", "diamantes", "money", "kivs", "atm", ou "bal" (opcional, padrão é ".").
        """
        if ctx.channel.id in self.channels:
            if arg.lower() in ["diamante", "diamantes", "money", "kivs", "atm", "bal"]:
                dados = get_rank("money")
                embed1, embeds = paginate_rank(
                    dados, len(dados), "Rank Kivs", my_key="money"
                )
                msg = await ctx.send(embed=embed1)
                page = Paginator(bot=self.bot, message=msg, embeds=embeds)
                await page.start()
            elif arg.lower() in ["vitorias", "vit", "c4", "connect4", "vitórias"]:
                dados = get_rank("c4")
                embed1, embeds = paginate_rank(
                    dados, len(dados), "Rank Vitórias", my_key="c4"
                )
                msg = await ctx.send(embed=embed1)
                page = Paginator(bot=self.bot, message=msg, embeds=embeds)
                await page.start()
            elif arg.lower() in ["rep", "reps"]:
                dados = get_rank("rep")
                embed1, embeds = paginate_rank(
                    dados, len(dados), "Rank Reps", my_key="rep"
                )
                msg = await ctx.send(embed=embed1)
                page = Paginator(bot=self.bot, message=msg, embeds=embeds)
                await page.start()
            elif arg.lower() in ["xp", "exp", "level", "nivel", "levels", "nível"]:
                dados = get_xp_rank()
                embed1, embeds = paginate_rank(
                    dados, len(dados), "Rank Xp", my_key="xp"
                )
                msg = await ctx.send(embed=embed1)
                page = Paginator(bot=self.bot, message=msg, embeds=embeds)
                await page.start()
            else:
                embed_rank = discord.Embed(
                    title=f"Consultar rank",
                    description=f"**Rank de kivs**: `{prefix}rank kivs`\n**Rank vitorias**: `{prefix}rank c4`\n**Rank reps**: `{prefix}rank reps`\n**Rank xp**: `{prefix}rank xp`\n",
                    colour=0xFFD301,
                )
                await ctx.send(embed=embed_rank)

    @commands.command()
    async def work(self, ctx) -> None:
        """Pegadinha para quem usa o comando errado"""
        if ctx.channel.id in self.channels:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/944649962686386256/983066514200616980/work.gif"
            )
            await ctx.send(
                "Work, work, work, work,work, work\nHe said me haffi work, work, work, work, work, work"
            )

    @commands.command(name="cooldown", aliases=["cd", "tempo"])
    @cooldown(1, 10, BucketType.user)
    async def cooldown(self, ctx) -> None:
        """
        Mostra informações sobre os cooldowns de diferentes comandos para o usuário.

        Parâmetros:
        ctx (commands.Context): O contexto da mensagem.
        """
        if ctx.channel.id in self.channels:
            today = get_days()
            date = get_daily(ctx.author.id)
            if date < today:
                daily = ":white_check_mark: Você já pode pegar seu daily."
            else:
                daily = "Você já pegou seu daily hoje."
            resp_rep = get_time_rep(ctx.author.id)
            if resp_rep == True:
                rep = ":white_check_mark: Você já pode dar rep."
            else:
                rep = f"Você deve esperar mais {resp_rep[:2]}m {resp_rep[3:]}s."
            n_apostas, time_a = get_cooldown_aposta(ctx.author.id)
            if n_apostas and time_a:
                apostar = f"Apostas: {n_apostas}/5 | Tempo pra zerar: {time_a[:2]}m {time_a[3:]}s."
            else:
                apostar = f":white_check_mark: Apostas: 0/5 | Você já pode fazer apostas `{prefix}apostar`."
            n_adivinhar, time_b = get_cooldown_guess(ctx.author.id)
            if n_adivinhar and time_b:
                adivinhar = f"Adivinhar: {n_adivinhar}/5 | Tempo pra zerar: {time_b[:2]}m {time_b[3:]}s."
            else:
                adivinhar = f":white_check_mark: Adivinhar: 0/5 | Você já pode adivinhar `{prefix}adivinhar`."
            cd_embed = discord.Embed(
                title=f"Cooldowns {ctx.author}",
                description=f"**Daily**\n{daily}\n\n**Rep**\n{rep}\n\n**Apostar**\n{apostar}\n\n**Adivinhar**\n{adivinhar}\n",
                colour=0xFFD301,
            )
            await ctx.send(embed=cd_embed)


def setup(bot):
    bot.add_cog(GeneralCog(bot))
