import discord
from random import randint
import asyncio
from discord.ext import commands
from db.cooldown import add_limit
from discord.ext.commands import cooldown, BucketType
from .funcoes import pass_to_num, get_prefix
from db.mydb import add_money

prefix = get_prefix()


class Game(commands.Cog):
    """
    Uma classe que define comandos relacionados a jogos.

    Esta classe fornece comandos para jogos e atividades de entretenimento.
    """

    def __init__(self, bot):
        """
        Inicializa uma instância da classe Game.

        Args:
            bot (commands.Bot): O objeto bot que representa o bot Discord.
        """
        self.bot = bot
        self.channels = []  # Lista de canais

    @commands.command(
        name="guess",
        aliases=["adv", "adivinhar", "adivinha", "chuta", "chutar"],
    )
    @cooldown(1, 8, BucketType.user)
    async def guess(self, ctx) -> None:
        """
        Inicia um jogo de adivinhação em que o usuário deve adivinhar um número de 1 a 100.

        O usuário tem quatro chances para acertar o número e ganhar prêmios em Kivs (moeda do jogo).
        A cada rodada, o bot informa se o número a ser adivinhado é maior ou menor do que o chute anterior.

        Args:
            ctx (commands.Context): O contexto da mensagem de comando.

        Returns:
            None
        """
        try:
            if (ctx.channel.id) in self.channels:

                def check(msg):
                    if msg.author == ctx.author:
                        return msg.content

                cd = add_limit(ctx.author.id)
                if cd == True:
                    guess_embed = discord.Embed(
                        title="Pensei em um número de 1 a 100",
                        description="**\nQue numero é esse?** Valendo 5.000:drop_of_blood: \nChance(1/4)",
                        colour=0xFFD301,
                    )
                    await ctx.send(embed=guess_embed)
                    num = randint(1, 100)

                    # Chance 1
                    response = await self.bot.wait_for(
                        "message", check=check, timeout=30
                    )
                    chute_1 = pass_to_num(response.content)
                    if chute_1:
                        if int(chute_1) == num:
                            await ctx.send(
                                f"Parabéns :tada: :tada: :tada: <@{ctx.author.id}> você acertou. Chance(1/4)\n**Você recebeu 5.000:drop_of_blood: **"
                            )
                            add_money(ctx.author.id, 5000)
                            return
                        elif int(chute_1) > num:
                            await ctx.send(
                                f"<@{ctx.author.id}> O número é **MENOR**. Chance(2/4)\nValendo 3.000:drop_of_blood: "
                            )
                        elif int(chute_1) < num:
                            await ctx.send(
                                f"<@{ctx.author.id}> O número é **MAIOR**. Chance(2/4)\nValendo 3.000:drop_of_blood: "
                            )
                    else:
                        await ctx.send("Resposta inválida. Digite apenas o número.")

                    # Chance 2
                    response = await self.bot.wait_for(
                        "message", check=check, timeout=30
                    )
                    chute_2 = pass_to_num(response.content)
                    if chute_2:
                        if int(chute_2) == num:
                            await ctx.send(
                                f"Parabéns :tada: :tada: :tada: <@{ctx.author.id}> você acertou. Chance(2/4)\n**Você recebeu 3.000:drop_of_blood: **"
                            )
                            add_money(ctx.author.id, 3000)
                            return
                        elif int(chute_2) > num:
                            await ctx.send(
                                f"<@{ctx.author.id}> O número é **MENOR**. Chance(3/4)\nValendo 2.000:drop_of_blood: "
                            )
                        elif int(chute_2) < num:
                            await ctx.send(
                                f"<@{ctx.author.id}> O número é **MAIOR**. Chance(3/4)\nValendo 2.000:drop_of_blood: "
                            )
                    else:
                        await ctx.send("Resposta inválida. Digite apenas o número.")

                    # Chance 3
                    response = await self.bot.wait_for(
                        "message", check=check, timeout=30
                    )
                    chute_3 = pass_to_num(response.content)
                    if chute_3:
                        if int(chute_3) == num:
                            await ctx.send(
                                f"Parabéns :tada: :tada: :tada: <@{ctx.author.id}> você acertou. Chance(3/4)\n**Você recebeu 2.000:drop_of_blood: **"
                            )
                            add_money(ctx.author.id, 2000)
                            return
                        elif int(chute_3) > num:
                            await ctx.send(
                                f"<@{ctx.author.id}> O número é **MENOR**. Chance(4/4)\nValendo 1.000:drop_of_blood: "
                            )
                        elif int(chute_3) < num:
                            await ctx.send(
                                f"<@{ctx.author.id}> O número é **MAIOR**. Chance(4/4)\nValendo 1.000:drop_of_blood: "
                            )
                    else:
                        await ctx.send("Resposta inválida. Digite apenas o número.")

                    # Chance 4
                    response = await self.bot.wait_for(
                        "message", check=check, timeout=30
                    )
                    chute_4 = pass_to_num(response.content)
                    if chute_4 and int(chute_4) == num:
                        await ctx.send(
                            f"Parabéns :tada: :tada: :tada: <@{ctx.author.id}> você acertou. Chance(4/4)\n**Você recebeu 1.000:drop_of_blood: **"
                        )
                        add_money(ctx.author.id, 1000)
                        return
                    else:
                        await ctx.send(
                            f"Era **{num}**. Você perdeu <@{ctx.author.id}>."
                        )
                        return
                else:
                    await ctx.send(f"Você precisa esperar mais {cd[:2]}m {cd[3:]}s")
            else:
                await ctx.send(
                    "Esse comando não é permitido aqui. Use em <#986033120568565760>"
                )
        except asyncio.TimeoutError:
            await ctx.send(f"<@{ctx.author.id}> Demorou demais. Game over")
            return


def setup(bot):
    """Load Game Cog."""
    bot.add_cog(Game(bot))
