from typing import List, Optional, Union
from pymongo import MongoClient
from decouple import config

MONGO_TOKEN = config("MONGO_TOKEN")

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["store"]


# ------------ Adiciona um novo item ------------------------
def add_item(
    name: str,
    cmd: str,
    desc: str,
    stock: str,
    price: int,
    role: Optional[str] = None,
    img: Optional[str] = None,
    msg: str = "",
) -> bool:
    """
    Adiciona um novo item à loja do bot.

    Args:
        name (str): O nome do item.
        cmd (str): O comando associado ao item.
        desc (str): A descrição do item.
        stock (str): A quantidade em estoque do item.
        price (int): O preço do item.
        role (str, optional): A função ou cargo associado ao item (opcional).
        img (str, optional): O link para uma imagem representando o item (opcional).
        msg (str): Uma mensagem associada ao item (opcional).

    Returns:
        bool: True se o item foi adicionado com sucesso, False se ocorreu um erro durante a adição.
    """
    try:
        dados = {
            "name": name,
            "cmd": cmd,
            "desc": desc,
            "stock": stock,
            "price": int(price),
            "role": role,
            "img": img,
            "msg": msg,
        }
        collection.insert_one(dados)
        return True
    except:
        return False


# ----------- Edita um item --------------
def edit_item(product_name: str, chave: str, valor: int) -> bool:
    """
    Edita um item na loja com base no nome do produto, uma chave e um valor para atualização.

    Args:
        product_name (str): O nome do produto que será editado.
        chave (str): A chave (atributo) que será atualizada.
        valor (int): O novo valor para a chave especificada.

    Returns:
        bool: True se o item foi editado com sucesso, False se ocorreu um erro durante a edição ou o item não foi encontrado.
    """
    if collection.find_one({"name": product_name}):
        try:
            product = collection.find_one({"name": product_name})
            newvalues = {"$set": {chave: valor}}
            collection.update_one(product, newvalues)
            return True
        except:
            return False
    else:
        return False


def remove_item(product_name: str) -> bool:
    """
    Remove um item da loja com base no nome do produto.

    Args:
        product_name (str): O nome do produto que será removido.

    Returns:
        bool: True se o item foi removido com sucesso, False se o item não foi encontrado.
    """
    if collection.find_one({"name": product_name}):
        collection.delete_one({"name": product_name})
        return True
    else:
        return False


def get_item(product_name: str, field: str = "name") -> Union[dict, bool]:
    """
    Obtém um item específico da loja pesquisando por um campo, com o campo padrão sendo "name".

    Args:
        product_name (str): O nome ou valor do campo a ser pesquisado.
        field (str, optional): O campo pelo qual a pesquisa será realizada (padrão: "name").

    Returns:
        Union[dict, bool]: Um dicionário representando o item se encontrado, ou False se não encontrado.
    """
    if collection.find_one({field: product_name}):
        return collection.find_one({field: product_name})
    else:
        return False


def get_all_items(query: Optional[str] = None) -> List[dict]:
    """
    Obtém todos os itens da loja ou itens específicos com base na consulta.

    Args:
        query (str, optional): A consulta para filtrar os itens (opcional).

    Returns:
        List[dict]: Uma lista de dicionários representando os itens correspondentes à consulta.
    """
    registers = list()
    if query is None:
        for x in collection.find().sort("name", 1):
            registers.append(x)
    elif query == "capas":
        for x in collection.find({"name": {"$regex": "^capa"}}).sort("name", 1):
            registers.append(x)
    elif query == "cores":
        for x in collection.find({"name": {"$regex": "^cor"}}).sort("name", 1):
            registers.append(x)
    elif query == "outro":
        for x in collection.find({"name": {"$not": {"$regex": "^cor|capa"}}}).sort(
            "name", 1
        ):
            registers.append(x)
    return registers
