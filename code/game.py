import discord
import numbers
import time
from random import randint
from discord.ext import commands
from db.cooldown import add_limit
from .funcoes import pass_to_num, get_prefix
from db.mydb import add_money

prefix = get_prefix()


class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channels = [944649962686386256]
        
    
    def is_channel(self, ctx):
        return ctx.channel.id == self.channel


    @commands.command(name="guess", aliases=["adv", "adivinhar", "adivinha", "chuta", "chutar"], )
    async def guess(self, ctx):
        
        if((ctx.channel.id) in self.channels):
            
            def check(msg):
                if msg.author == ctx.author:
                    return msg.content
            cd = add_limit(ctx.author.id)
            if cd == True:
                guess_embed = discord.Embed(title="Adivinhe o número", description="Prêmio: 4.000<:diamantt:973404655050719232>ㅤㅤㅤㅤㅤChances: 4", colour=0xFFD301)
                guess_embed.add_field(name="ㅤ", value="**Pensei em um número de 1 a 100\nQue numero é esse?**")
                await ctx.send(embed=guess_embed)
                num = randint(1, 100)

                # Chance 1
                response = await self.bot.wait_for("message", check=check, timeout=30)
                chute_1 = pass_to_num(response.content)
                if isinstance(chute_1, numbers.Integral):
                    if int(chute_1) == num:
                        await ctx.send(f"Parabéns <@{ctx.author.id}> você acertou. Chance(1/4)")
                        add_money(ctx.author.id, 4000)
                        return
                    elif int(chute_1) > num:
                        await ctx.send(f"<@{ctx.author.id}> O número é **MENOR**. Chance(1/4)")
                    elif int(chute_1) < num:
                        await ctx.send(f"<@{ctx.author.id}> O número é **MAIOR**. Chance(1/4)")
                else:
                    await ctx.send("Resposta inválida. Digite apenas o número.")
                
                # Chance 2
                response = await self.bot.wait_for("message", check=check, timeout=30)
                chute_2 = pass_to_num(response.content)
                if isinstance(chute_2, numbers.Integral):
                    if int(chute_2) == num:
                        await ctx.send(f"Parabéns <@{ctx.author.id}> você acertou. Chance(2/4)")
                        add_money(ctx.author.id, 4000)
                        return
                    elif int(chute_2) > num:
                        await ctx.send(f"<@{ctx.author.id}> O número é **MENOR**. Chance(2/4)")
                    elif int(chute_2) < num:
                        await ctx.send(f"<@{ctx.author.id}> O número é **MAIOR**. Chance(2/4)")
                else:
                    await ctx.send("Resposta inválida. Digite apenas o número.") 
                
                # Chance 3
                response = await self.bot.wait_for("message", check=check, timeout=30)
                chute_3 = pass_to_num(response.content)
                if isinstance(chute_3, numbers.Integral):
                    if int(chute_3) == num:
                        await ctx.send(f"Parabéns <@{ctx.author.id}> você acertou. Chance(3/4)")
                        add_money(ctx.author.id, 4000)
                        return
                    elif int(chute_3) > num:
                        await ctx.send(f"<@{ctx.author.id}> O número é **MENOR**. Chance(3/4)")
                    elif int(chute_3) < num:
                        await ctx.send(f"<@{ctx.author.id}> O número é **MAIOR**. Chance(3/4)")
                else:
                    await ctx.send("Resposta inválida. Digite apenas o número.")

                # Chance 4               
                response = await self.bot.wait_for("message", check=check, timeout=30)
                chute_4 = pass_to_num(response.content)
                if isinstance(chute_4, numbers.Integral) and int(chute_4) == num:
                    await ctx.send(f"Parabéns <@{ctx.author.id}> você acertou. Chance(4/4)")
                    add_money(ctx.author.id, 4000)
                    return
                else:
                    await ctx.send(f"O número era {num}. Você perdeu <@{ctx.author.id}>.")
                    return
            else:
                await ctx.send(f"Você precisa esperar mais {cd[:2]}m {cd[3:]}s")
        else:
            original = ("erro", "1")
            raise commands.CommandInvokeError(original)



	
def setup(bot):
    """Load Game Cog."""
    bot.add_cog(Game(bot))

'''    @guess.error
    async def guess_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("aiaiai")'''