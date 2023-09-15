# Cria as paginações
from typing import List, Tuple
import discord
import math
from .funcoes import get_prefix, remove_png, pass_to_money

prefix = get_prefix()


def paginate_rank(volume: list, size: int, embed_title: str, my_key: str) -> tuple:
    """
    Pagina os rankings de dinheiro e C4 em uma lista de embeds.

    Esta função cria uma lista de embeds para exibir rankings divididos em páginas. Cada página contém 10 entradas.

    Args:
        volume (list): Uma lista contendo as entradas do ranking.
        size (int): O número total de entradas no ranking.
        embed_title (str): O título que será usado em todos os embeds.
        my_key (str): A chave usada para identificar a classificação do usuário atual.

    Returns:
        tuple: Um objeto de embed representando a primeira página e uma lista de objetos de embed representando as
               páginas subsequentes.
    """
    lista_de_embed = []
    paginas = math.ceil(size / 10)
    if paginas > 10:
        paginas = 10
    description_1 = volume[:10]
    embed_1 = discord.Embed(
        title=embed_title,
        description=create_rank(description_1, my_key),
        colour=0xFFD301,
    )
    footer = f"Página 1 de {paginas}"
    embed_1.set_footer(text=footer)
    lista_de_embed.append(embed_1)
    if size > 10:
        description_2 = volume[10:20]
        embed_2 = discord.Embed(
            title=embed_title,
            description=create_rank(description_2, my_key, num=11),
            colour=0xFFD301,
        )
        footer = f"Página 2 de {paginas}"
        embed_2.set_footer(text=footer)
        lista_de_embed.append(embed_2)
    if size > 20:
        description_3 = volume[20:30]
        embed_3 = discord.Embed(
            title=embed_title,
            description=create_rank(description_3, my_key, num=21),
            colour=0xFFD301,
        )
        footer = f"Página 3 de {paginas}"
        embed_3.set_footer(text=footer)
        lista_de_embed.append(embed_3)
    if size > 30:
        description_4 = volume[30:40]
        embed_4 = discord.Embed(
            title=embed_title,
            description=create_rank(description_4, my_key, num=31),
            colour=0xFFD301,
        )
        footer = f"Página 4 de {paginas}"
        embed_4.set_footer(text=footer)
        lista_de_embed.append(embed_4)
    if size > 40:
        description_5 = volume[40:50]
        embed_5 = discord.Embed(
            title=embed_title,
            description=create_rank(description_5, my_key, num=41),
            colour=0xFFD301,
        )
        footer = f"Página 5 de {paginas}"
        embed_5.set_footer(text=footer)
        lista_de_embed.append(embed_5)
    if size > 50:
        description_6 = volume[50:60]
        embed_6 = discord.Embed(
            title=embed_title,
            description=create_rank(description_6, my_key, num=51),
            colour=0xFFD301,
        )
        footer = f"Página 6 de {paginas}"
        embed_6.set_footer(text=footer)
        lista_de_embed.append(embed_6)
    if size > 60:
        description_7 = volume[60:70]
        embed_7 = discord.Embed(
            title=embed_title,
            description=create_rank(description_7, my_key, num=61),
            colour=0xFFD301,
        )
        footer = f"Página 7 de {paginas}"
        embed_7.set_footer(text=footer)
        lista_de_embed.append(embed_7)
    if size > 70:
        description_8 = volume[70:80]
        embed_8 = discord.Embed(
            title=embed_title,
            description=create_rank(description_8, my_key, num=71),
            colour=0xFFD301,
        )
        footer = f"Página 8 de {paginas}"
        embed_8.set_footer(text=footer)
        lista_de_embed.append(embed_8)
    if size > 80:
        description_9 = volume[80:90]
        embed_9 = discord.Embed(
            title=embed_title,
            description=create_rank(description_9, my_key, num=81),
            colour=0xFFD301,
        )
        footer = f"Página 9 de {paginas}"
        embed_9.set_footer(text=footer)
        lista_de_embed.append(embed_9)
    if size > 90:
        description_10 = volume[90:100]
        embed_10 = discord.Embed(
            title=embed_title,
            description=create_rank(description_10, my_key, num=91),
            colour=0xFFD301,
        )
        footer = f"Página 10 de 10"
        embed_10.set_footer(text=footer)
        lista_de_embed.append(embed_10)
    return embed_1, lista_de_embed


def create_rank(dates: list, my_key: str, num: int = 1) -> str:
    """
    Cria uma representação em formato de string de um ranking.

    Esta função cria uma string que representa um ranking baseado nos dados fornecidos. O formato da string
    depende da chave especificada em `my_key`.

    Args:
        dates (list): Uma lista de dicionários contendo os dados das entradas do ranking.
        my_key (str): A chave usada para determinar como formatar o ranking.
        num (int, opcional): O número inicial para a classificação das entradas no ranking. O padrão é 1.

    Returns:
        str: Uma string representando o ranking formatado.
    """
    if my_key == "c4":
        rank_ordenado = ""
        for item in dates:
            rank_ordenado += str(
                f'**{num}.** <@{item["_id"]}> \t **{item[my_key]}** Vitórias\n'
            )
            num += 1
        return rank_ordenado
    elif my_key == "money":
        rank_ordenado = ""
        for item in dates:
            rank_ordenado += str(
                f'**{num}.** <@{item["_id"]}>\t\t**{pass_to_money(item["money"])}:drop_of_blood: **\n'
            )
            num += 1
    elif my_key == "rep":
        rank_ordenado = ""
        for item in dates:
            rank_ordenado += str(
                f'**{num}.** <@{item["_id"]}>\t\t**{item["rep"]} Reps**\n'
            )
            num += 1
    elif my_key == "xp":
        rank_ordenado = ""
        for item in dates:
            rank_ordenado += str(
                f'**{num}.** <@{item["_id"]}>\t**Level** {item["level"]}\n'
            )
            num += 1
    elif my_key == "milho":
        rank_ordenado = ""
        for item in dates:
            rank_ordenado += str(
                f'**{num}.** **<@{item["_id"]}>\t** {item["milho"]}:corn:\n'
            )
            num += 1
    return rank_ordenado


def paginate_store(
    volume: list, size: int, embed_title: str
) -> Tuple[discord.Embed, List[discord.Embed]]:
    """
    Realiza a paginação de itens de uma loja.

    Esta função cria uma lista de objetos Embed do Discord que representam páginas de itens da loja.

    Args:
        volume (list): Uma lista de itens da loja.
        size (int): O tamanho total da lista de itens.
        embed_title (str): O título a ser usado nos Embeds da loja.

    Returns:
        Tuple[discord.Embed, List[discord.Embed]]: Um objeto Embed representando a primeira página da loja e uma lista
        de Embeds representando as páginas subsequentes.
    """
    paginas = math.ceil(size / 9)
    lista_de_embed = []
    items = volume[:9]
    embed_1 = discord.Embed(
        title="Loja " + embed_title,
        description=f"Use os comandos de info para mais detalhes do item.\n\n",
        colour=0xFFD301,
    )
    for i in items:
        if ".png" in i["name"]:
            name = i["name"].replace(".png", "")
        else:
            name = i["name"]
        if i["role"]:
            embed_1.add_field(
                name=f"{name.capitalize()}",
                value=f"Cargo: <@&{i['role']}>\n`{prefix}info {i['cmd']}`\n",
                inline=False,
            )
        else:
            embed_1.add_field(
                name=f"{name.capitalize()}",
                value=f"`{prefix}info {i['cmd']}`",
                inline=False,
            )
    embed_1.add_field(
        name="Você pode filtrar",
        value=f"`{prefix}loja capas` | `{prefix}loja cores` | `{prefix}loja outros`",
    )
    footer = f"Página 1 de {paginas}"
    embed_1.set_footer(text=footer)
    embed_1.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/883810728140734506/977984460081475675/istockphoto-1152401093-612x612.jpg"
    )
    lista_de_embed.append(embed_1)
    if size > 9:
        items = volume[9:18]
        embed_2 = discord.Embed(
            title="Loja " + embed_title, description="", colour=0xFFD301
        )
        for i in items:
            if ".png" in i["name"]:
                name = i["name"].replace(".png", "")
            else:
                name = i["name"]
            if i["role"]:
                embed_2.add_field(
                    name=f"{name.capitalize()}",
                    value=f"Cargo: <@&{i['role']}>\n`{prefix}info {i['cmd']}`\n",
                    inline=False,
                )
            else:
                embed_2.add_field(
                    name=f"{name.capitalize()}",
                    value=f"`{prefix}info {i['cmd']}`",
                    inline=False,
                )

        footer = f"Página 2 de {paginas}"
        embed_2.set_footer(text=footer)
        embed_2.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/883810728140734506/977984460081475675/istockphoto-1152401093-612x612.jpg"
        )
        lista_de_embed.append(embed_2)
    if size > 18:
        items = volume[18:27]
        embed_3 = discord.Embed(
            title="Loja " + embed_title, description="", colour=0xFFD301
        )
        for i in items:
            if ".png" in i["name"]:
                name = i["name"].replace(".png", "")
            else:
                name = i["name"]
            if i["role"]:
                embed_3.add_field(
                    name=f"{name.capitalize()}",
                    value=f"Cargo: <@&{i['role']}>\n`{prefix}info {i['cmd']}`\n",
                    inline=False,
                )
            else:
                embed_3.add_field(
                    name=f"{name.capitalize()}",
                    value=f"`{prefix}info {i['cmd']}`",
                    inline=False,
                )
        footer = f"Página 3 de {paginas}"
        embed_3.set_footer(text=footer)
        embed_3.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/883810728140734506/977984460081475675/istockphoto-1152401093-612x612.jpg"
        )
        lista_de_embed.append(embed_3)
    if size > 27:
        items = volume[27:36]
        embed_4 = discord.Embed(
            title="Loja " + embed_title, description="", colour=0xFFD301
        )
        for i in items:
            if ".png" in i["name"]:
                name = i["name"].replace(".png", "")
            else:
                name = i["name"]
            if i["role"]:
                embed_4.add_field(
                    name=f"{name.capitalize()}",
                    value=f"Cargo: <@&{i['role']}>\n`{prefix}info {i['cmd']}`\n",
                    inline=False,
                )
            else:
                embed_4.add_field(
                    name=f"{name.capitalize()}",
                    value=f"`{prefix}info {i['cmd']}`",
                    inline=False,
                )
        footer = f"Página 4 de {paginas}"
        embed_4.set_footer(text=footer)
        embed_4.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/883810728140734506/977984460081475675/istockphoto-1152401093-612x612.jpg"
        )
        lista_de_embed.append(embed_4)
    if size > 36:
        items = volume[36:45]
        embed_5 = discord.Embed(
            title="Loja " + embed_title, description="", colour=0xFFD301
        )
        for i in items:
            if ".png" in i["name"]:
                name = i["name"].replace(".png", "")
            else:
                name = i["name"]
            if i["role"]:
                embed_5.add_field(
                    name=f"{name.capitalize()}",
                    value=f"Cargo: <@&{i['role']}>\n`{prefix}info {i['cmd']}`\n",
                    inline=False,
                )
            else:
                embed_5.add_field(
                    name=f"{name.capitalize()}",
                    value=f"`{prefix}info {i['cmd']}`",
                    inline=False,
                )
        footer = f"Página 5 de {paginas}"
        embed_5.set_footer(text=footer)
        embed_5.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/883810728140734506/977984460081475675/istockphoto-1152401093-612x612.jpg"
        )
        lista_de_embed.append(embed_5)
    if size > 45:
        items = volume[45:54]
        embed_6 = discord.Embed(
            title="Loja " + embed_title, description="", colour=0xFFD301
        )
        for i in items:
            if ".png" in i["name"]:
                name = i["name"].replace(".png", "")
            else:
                name = i["name"]
            if i["role"]:
                embed_6.add_field(
                    name=f"{name.capitalize()}",
                    value=f"Cargo: <@&{i['role']}>\n`{prefix}info {i['cmd']}`\n",
                    inline=False,
                )
            else:
                embed_6.add_field(
                    name=f"{name.capitalize()}",
                    value=f"`{prefix}info {i['cmd']}`",
                    inline=False,
                )
        footer = f"Página 6 de {paginas}"
        embed_6.set_footer(text=footer)
        embed_6.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/883810728140734506/977984460081475675/istockphoto-1152401093-612x612.jpg"
        )
        lista_de_embed.append(embed_6)
    return embed_1, lista_de_embed
