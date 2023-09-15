import discord
from io import BytesIO
import textwrap as tr
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from PIL import Image, ImageChops, ImageDraw, ImageFont
from db.mydb import (
    get_user,
    get_time_rep_and_add,
    add_rep,
    get_user_capas,
    set_capa,
    set_status,
    get_user_cores,
    set_cor,
)
from code.funcoes import (
    get_prefix,
    pass_to_date,
    pass_to_money,
    find_capa,
    get_id,
    all_channels,
    find_cor,
)
from .rank_xp import get_xp_user
from .asserts import lista_de_cores

prefix = get_prefix()


class Information(commands.Cog):
    """
    Comandos de informações, incluindo perfil, cores, capas e status.
    """

    def __init__(self, bot):
        self.bot = bot
        self.channels = all_channels()

    @classmethod
    def circle(cls, pfp: Image.Image, size=(220, 220)) -> Image.Image:
        """
        Redimensiona e enmascara uma imagem de perfil para criar uma imagem circular.

        Args:
            pfp (Image.Image): A imagem de perfil a ser processada.
            size (tuple, opcional): O tamanho final da imagem. Padrão é (220, 220).

        Returns:
            Image.Image: Uma imagem redimensionada e emmascarada em formato circular.
        """
        pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(pfp.size, Image.ANTIALIAS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)
        return pfp

    @commands.command(name="profile", aliases=["perfil", "p"])
    @cooldown(1, 6, BucketType.user)
    async def profile(self, ctx, member=None) -> None:
        """
        Exibe o perfil de um usuário, incluindo informações como nome, dinheiro, reputação, etc.

        Args:
            ctx (commands.Context): O contexto do comando.
            member (str, opcional): O membro cujo perfil será exibido. Padrão é o autor do comando.
        """
        if ctx.channel.id in self.channels:
            if member is None:
                member = ctx.author
            else:
                member1 = get_id(member)
                member = ctx.guild.get_member(member1)
            if member == None or member.bot:
                await ctx.send("¯\_(ツ)_/¯ Não encontrei essa pessoa no servidor.")
                return
            info = get_user(member.id)
            level, xp = get_xp_user(member.id)
            name = str(member.display_name)
            if info:
                money = pass_to_money(info["money"])
                rep = str(info["rep"]) + " reps"
                frase = tr.wrap(str(info["status"]), width=60)
                sobremim = "\n".join(frase)
                vip = pass_to_date(info["vip"])
                vits = str(info["c4"]) + " Vitórias"
                user_bg = str(info["capa"].replace("capa", ""))
            else:
                money, rep, vits, vip = "0", "0 Reps", "0 Vitórias", "-"
                frase = tr.wrap(
                    f"Use {prefix}status <frase> para alterar aqui", width=60
                )
                sobremim = "\n".join(frase)
                user_bg = "default.png"

            base = Image.open("capas/base.png").convert("RGBA")
            background = Image.open("capas/" + user_bg).convert("RGBA")

            pfp = member.avatar_url_as(size=256)
            data = BytesIO(await pfp.read())
            pfp = Image.open(data).convert("RGBA")

            name = f"{name[:16]}.." if len(name) > 16 else name
            sobremim = f"{sobremim[:111]}.." if len(sobremim) > 111 else sobremim

            draw = ImageDraw.Draw(base)
            pfp = self.circle(pfp, (220, 220))
            font = ImageFont.truetype("capas/Nunito-Regular.ttf", 38)
            subfont = ImageFont.truetype("capas/Nunito-Regular.ttf", 25)

            draw.text((280, 240), name, font=font)
            draw.text((25, 380), sobremim, font=subfont)
            draw.text((60, 530), money, font=subfont)
            draw.text((410, 532), vits, font=subfont)
            draw.text((60, 655), rep, font=subfont)
            draw.text((410, 655), vip, font=subfont)
            draw.text((60, 780), level, font=subfont)
            draw.text((410, 780), xp, font=subfont)
            base.paste(pfp, (56, 158), pfp)
            background.paste(base, (0, 0), base)

            with BytesIO() as a:
                background.save(a, "PNG")
                a.seek(0)
                await ctx.send(file=discord.File(a, "profile.png"))

    @profile.error
    async def profile_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.channel.id in self.channels:
                await ctx.send(
                    f"Você deve esperar alguns segundos para usar este comando."
                )

    @commands.command()
    async def rep(self, ctx, member) -> None:
        """
        Dá uma reputação a outro membro do servidor.

        Args:
            ctx (commands.Context): O contexto do comando.
            member (str): O membro para o qual a reputação será dada.
        """
        if ctx.channel.id in self.channels:
            try:
                member = get_id(member)
                user = ctx.guild.get_member(member)
                if user and ctx.author.id != user.id and not (user.bot):
                    response = get_time_rep_and_add(ctx.author.id)
                    if response == True:
                        add_rep(user.id)
                        await ctx.send(f"{ctx.author} acaba de dar uma rep para {user}")
                    else:
                        await ctx.send(
                            f"Você precisa esperar mais {response[:2]}m {response[3:]}s"
                        )
            except:
                return

    @commands.command()
    async def usar(self, ctx, *, arg: str = "") -> None:
        """
        Altera a cor ou capa do perfil do usuário.

        Args:
            ctx (commands.Context): O contexto do comando.
            arg (str, opcional): A ação a ser executada, como "cor" ou "capa". Padrão é vazio.
        """
        if ctx.channel.id in self.channels:
            arg = arg.lower()
            if "cor" in arg:
                arg = arg.replace("cor", "")
                cor = find_cor(str(arg.strip()))
                user_cores = get_user_cores(ctx.author.id)
                if user_cores and cor:
                    msg = await ctx.send(f"Só 1 min")
                    for i in user_cores:
                        if i == cor:
                            member = ctx.guild.get_member(ctx.author.id)
                            for role in lista_de_cores:
                                role_get = get(member.guild.roles, id=role)
                                await member.remove_roles(role_get)
                            cor_nova = ctx.guild.get_role(cor)
                            await member.add_roles(cor_nova)
                            await ctx.send("Cor alterada com sucesso.")
                            await msg.delete()
                            return
                elif not cor:
                    await ctx.send(
                        f"Não encontrei essa cor. Use {prefix}cores e veja se ela faz parte das suas cores."
                    )
                elif not user_cores:
                    await ctx.send("Você ainda não comprou nenhuma cor.")
            elif "capa" in arg:
                arg = arg.replace("capa", "")
                capa = find_capa(arg.strip())
                user_capas = get_user_capas(ctx.author.id)
                if user_capas and capa:
                    for i in user_capas:
                        if i == capa:
                            set_capa(ctx.author.id, capa)
                            await ctx.send("Capa alterada com sucesso.")
                            return
                elif not capa:
                    await ctx.send(
                        f"Não encontrei essa capa. Use {prefix}capas e veja se ela faz parte das suas capas."
                    )
                elif not user_capas:
                    await ctx.send("Você ainda não comprou nenhuma capa.")
            else:
                usar_embed = discord.Embed(
                    title="Usar",
                    description=f"`{prefix}usar cor <nome>` Altera sua cor.\n`{prefix}usar capa <nome>` Altera sua capa.\n",
                    colour=0xFFD301,
                )
                await ctx.send(embed=usar_embed)

    @commands.command(name="cores", aliases=["cor", "color"])
    async def cores(self, ctx) -> None:
        """
        Exibe as cores disponíveis para o perfil do usuário.

        Args:
            ctx (commands.Context): O contexto do comando.
        """
        if ctx.channel.id in self.channels:
            user_cores = get_user_cores(ctx.author.id)
            description = f"**Para usar a cor utilize** `{prefix}usar cor <nome>`\n**Não** precisa do @\n\n"
            if len(user_cores) > 0:
                user_cores.sort()
                for x in user_cores:
                    description += f"<@&{x}>\n"
                embed_cores = discord.Embed(
                    title=f"Cores de {ctx.author}",
                    description=description,
                    colour=0xFFD301,
                )
                await ctx.send(embed=embed_cores)
            else:
                embed_cores = discord.Embed(
                    title=f"Cores de {ctx.author}",
                    description=f"Você ainda não possui cores. Use `{prefix}loja`",
                    colour=0xFFD301,
                )
                await ctx.send(embed=embed_cores)

    @commands.command(
        name="capas",
        aliases=["capa", "background", "wallpaper", "backgrounds", "wallpapers"],
    )
    async def capas(self, ctx) -> None:
        """
        Exibe as capas disponíveis para o perfil do usuário.

        Args:
            ctx (commands.Context): O contexto do comando.
        """
        if ctx.channel.id in self.channels:
            user_capas = get_user_capas(ctx.author.id)
            description = f"**Para usar a capa utilize** `{prefix}usar capa <nome>`\n\n"
            if len(user_capas) > 1:
                user_capas.sort()
                for x in user_capas:
                    if x not in "default.png":
                        x = x.replace(".png", "\n")
                        x = x.replace("capa", "")
                        description += x
                embed_capas = discord.Embed(
                    title=f"Capas de {ctx.author}",
                    description=description,
                    colour=0xFFD301,
                )
                await ctx.send(embed=embed_capas)
            else:
                embed_capas = discord.Embed(
                    title=f"Capas de {ctx.author}",
                    description=f"Você ainda não possui capas. Use `{prefix}loja`",
                    colour=0xFFD301,
                )
                await ctx.send(embed=embed_capas)

    @commands.command()
    async def status(self, ctx, *, arg: str = "") -> None:
        """
        Define um status personalizado para o perfil do usuário.

        Args:
            ctx (commands.Context): O contexto do comando.
            arg (str, opcional): O status personalizado a ser definido. Padrão é vazio.
        """
        if ctx.channel.id in self.channels:
            set_status(ctx.author.id, arg)
            await ctx.send("Status alterado.")


def setup(bot):
    bot.add_cog(Information(bot))
