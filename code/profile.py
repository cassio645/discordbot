import discord
from io import BytesIO
import textwrap as tr
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from PIL import Image, ImageChops, ImageDraw, ImageFont
from db.mydb import get_user, get_time_rep, add_rep, get_user_capas, set_capa, set_status
from code.funcoes import get_prefix, pass_to_date, pass_to_money, find_capa, get_id
from .rank_xp import get_xp_user

prefix = get_prefix()


def circle(pfp, size=(220, 220)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] *3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


class Information(commands.Cog):
    """Information commands regarding leaderboard, server, Image profile"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="profile", aliases=["perfil", "p"])
    @cooldown(1, 6, BucketType.user)
    async def profile(self, ctx, member=None):
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
            user_bg = str(info["capa"])  
        else:
            money, rep, vits, vip = "0", "0 Reps", "0 Vitórias", "-"
            frase = tr.wrap(f"Use {prefix}status <frase> para alterar aqui", width=60)
            sobremim = "\n".join(frase)
            user_bg = "default.png"

        base = Image.open("capas/base.png").convert("RGBA")
        background = Image.open("capas/" + user_bg).convert("RGBA")

        pfp = member.avatar_url_as(size=256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")

        name =  f"{name[:16]}.." if len(name)>16 else name
        sobremim = f"{sobremim[:111]}.." if len(sobremim)>111 else sobremim

        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, (220, 220))
        font = ImageFont.truetype("capas/Nunito-Regular.ttf", 38)
        subfont = ImageFont.truetype("capas/Nunito-Regular.ttf", 25)

        draw.text((280, 240), name, font=font)
        draw.text((25, 380), sobremim, font=subfont)
        draw.text((60, 530), money, font=subfont)
        draw.text((410, 530), vits, font=subfont)
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
            await ctx.send(f'Você deve esperar alguns segundos para usar este comando.')


    @commands.command()
    async def rep(self, ctx, member):
        try:
            member = get_id(member)
            user = ctx.guild.get_member(member)
            if user and ctx.author.id != user.id and not(user.bot):
                response = get_time_rep(ctx.author.id)
                if response == True:
                    add_rep(user.id)
                    await ctx.send(f"{ctx.author} acaba de dar uma rep para {user}")
                else:
                    await ctx.send(f'Você precisa esperar mais {response[:2]}m {response[3:]}s')
        except:
            return
        
    @commands.command()
    async def usar(self, ctx, *, arg):
        capa = find_capa(str(arg))
        user_capas = get_user_capas(ctx.author.id)
        if user_capas and capa:
            for i in user_capas:
                if i == capa:
                    set_capa(ctx.author.id, capa)
                    await ctx.send("Capa alterada com sucesso.")
                    return
        elif not capa:
            await ctx.send(f"Não encontrei essa capa. Use {prefix}capas e veja se ela faz parte das suas capas.")
        elif not user_capas:
            await ctx.send("Você ainda não comprou nenhuma capa.")



    @commands.command(name="capas", aliases=["capa", "background", "wallpaper", "backgrounds", "wallpapers"])
    async def capas(self, ctx):
        user_capas = get_user_capas(ctx.author.id)
        description = f'**Para usar a capa utilize** `{prefix}usar <nome>`\n\n'
        if len(user_capas) > 1:
            user_capas.sort()
            for x in user_capas:
                if x not in "default.png":
                    description += x.replace(".png", "\n")
            embed_capas = discord.Embed(title=f"Capas de {ctx.author}", description=description, colour=0xFFD301)
            await ctx.send(embed=embed_capas)
        else:
            embed_capas = discord.Embed(title=f"Capas de {ctx.author}", description=f"Você ainda não possui capas. Use `{prefix}loja`", colour=0xFFD301)
            await ctx.send(embed=embed_capas)


    @commands.command()
    async def status(self, ctx, *, arg=""):
        set_status(ctx.author.id, arg)
        await ctx.send("Status alterado.")

        
def setup(bot):
	bot.add_cog(Information(bot))