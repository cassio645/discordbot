import discord
from discord.ext import commands
from random import randint, choice
from asyncio import TimeoutError

from pymongo import MongoClient
from decouple import config
from time import sleep

from .funcoes import get_id, get_prefix, pass_to_money

prefix = get_prefix()

MONGO_TOKEN = config("MONGO_TOKEN")

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["msg"]

# Nivel de exp para cada level
levels = [
    10,
    100,
    200,
    300,
    500,
    800,
    1300,
    2100,
    3400,
    5500,
    7700,
    10000,
    12400,
    14900,
    17500,
    20200,
    23000,
    25900,
    28900,
    32000,
    35200,
    38500,
    41900,
    45400,
    49000,
    52700,
    56500,
    60400,
    64400,
    68500,
    72700,
    77000,
    81400,
    85900,
    90500,
    95200,
    100000,
    104900,
    109900,
    115000,
    120200,
    125500,
    130900,
    136400,
    142000,
    147700,
    153500,
    159400,
    165400,
    171500,
    177700,
    184000,
    190400,
    196900,
    203500,
    210200,
    217000,
    223900,
    230900,
    238000,
    245200,
    252500,
    259900,
    267400,
    275000,
    282700,
    290500,
    298400,
    306400,
    314500,
    322700,
    331000,
    339400,
    347900,
    356500,
    365200,
    374000,
    382900,
    391900,
    401000,
    410200,
    419500,
    428900,
    438400,
    448000,
    457700,
    467500,
    477400,
    487400,
    497500,
    507700,
    518000,
    528400,
    538900,
    549500,
    560200,
    571000,
    581900,
    592900,
    604000,
]


def all_channels() -> list:
    """
    Retorna uma lista de IDs de canais onde o xp dos usuários deve ser contada.

    Returns:
        list: Uma lista de IDs de canais.
    """
    return []  # Preencha esta lista com os IDs dos canais desejados.


def level_up(user_id: int, level: int) -> None:
    """
    Atualiza o nível de um usuário no banco de dados.

    Args:
        user_id (int): O ID do usuário que terá seu nível atualizado.
        level (int): O novo nível do usuário.
    """
    user = collection.find_one({"_id": user_id})
    level += 1
    update_level = {"$set": {"level": level}}
    collection.update_one(user, update_level)


def get_xp_rank() -> list:
    """
    Obtém a lista de registros do rank de experiência ordenados pelo nível.

    Returns:
        list: Uma lista de registros do rank de experiência ordenados pelo nível.
    """
    registers = list()
    # Consulta o rank completo e ordena pela ordem de xp
    for i in collection.find({"level": {"$gt": 0}}).sort("level", -1):
        registers.append(i)
    return registers


def get_xp_user(user_id: int) -> tuple:
    """
    Obtém o nível e a quantidade de experiência de um usuário.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        tuple: Uma tupla contendo o nível e a quantidade de experiência do usuário.
               O formato da tupla é (str, str), onde o primeiro elemento é o nível e
               o segundo elemento é a quantidade de experiência no formato "X/Y xp".
    """
    try:
        info = collection.find_one({"_id": user_id})
        level = "Level " + str(info["level"])
        xp = (
            str(pass_to_money(info["xp"]))
            + "/"
            + str(pass_to_money(levels[info["level"]]))
            + " xp"
        )
        return level, xp
    except:
        return "Level 0", "0/10 xp"


def delete_xp(user_id: int) -> None:
    """
    Apaga os dados de experiência de um usuário.

    Args:
        user_id (int): O ID do usuário cujos dados de experiência devem ser apagados.

    Returns:
        None: Esta função não retorna nenhum valor.
    """
    try:
        collection.delete_one({"_id": user_id})
    except:
        pass


class Rank(commands.Cog):
    """
    Uma classe de cog (módulo) que lida com o sistema de experiência e níveis.

    Esta classe é responsável por atualizar a experiência dos usuários e gerenciar os níveis dos usuários.
    """

    def __init__(self, bot):
        """
        Inicializa uma instância da classe Rank.

        Args:
            bot (discord.ext.commands.Bot): O bot Discord utilizado para registrar os comandos.
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx) -> None:
        """
        Um listener (ouvinte) usado para contar cada mensagem que cada usuário envia.

        Este listener lida com a atribuição de experiência aos usuários e atualização de seus níveis com base nas mensagens enviadas.

        Args:
            ctx (discord.Message): O objeto da mensagem enviada.
        """
        if ctx.channel.id in all_channels():
            sleep(1)
            await ctx.delete()
        user_id = ctx.author.id
        if ctx.author.bot:
            return
        xp = [0, 0, 1, 2, 5, 10]
        xp = choice(xp)
        if xp > 0:
            if collection.find_one({"_id": user_id}):
                user = collection.find_one({"_id": user_id})
                newxp = (user["xp"]) + xp
                newvalues = {"$set": {"xp": newxp}}
                collection.update_one(user, newvalues)
                if newxp >= levels[user["level"]]:
                    level_up(user_id, user["level"])
            else:
                dados = {"_id": user_id, "level": 0, "xp": xp}
                collection.insert_one(dados)


'''
@commands.command(name="reset_xp", aliases=["reset-xp", "resete-xp", "resete_xp"])
@commands.has_permissions(administrator=True)
async def reset_xp(self, ctx):
    """
    Reseta a experiência (XP) de todos os usuários do servidor.

    Este comando só pode ser executado por administradores do servidor e irá apagar a experiência de todos os usuários que tenham pelo menos 1 ponto de XP.

    Args:
        ctx (discord.ext.commands.Context): O contexto do comando.
    """
    if collection.delete_many({"xp": {"$gt": 0}}):
        await ctx.send("O XP do servidor foi resetado.")
    else:
        await ctx.send("Não foi possível resetar o XP do servidor.")

'''


def setup(bot):
    """Load Rank Cog."""
    bot.add_cog(Rank(bot))
