from pymongo import MongoClient
from decouple import config
from pymongo.errors import DuplicateKeyError

MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Discord"]
collection = db["store"]


# ------------ Adiciona um novo item ------------------------
def add_item(name:str, cmd:str, desc:str, stock:str, price:int, role=None, img=None, msg="") -> bool:
    try:
        dados = {
            "name": name,
            "cmd": cmd,
            "desc": desc,
            "stock": stock,
            "price": int(price),
            "role": role,
            "img": img,
            "msg": msg
        }
        collection.insert_one(dados)
        return True
    except:
        return False

# ----------- Edita um item --------------
def edit_item(product_name, chave, valor):
    # recebe o Id, uma chave e valor para criar um dicionário com os novos valores
    if collection.find_one({"name": product_name}):
        try:
            product = collection.find_one({"name": product_name})
            newvalues = { "$set": {chave: valor} }
            collection.update_one(product, newvalues)
            return True
        except:
            return False
    else:
        return False

def remove_item(product_name):
    # apaga um item da loja
    if collection.find_one({"name": product_name}):
        collection.delete_one({"name": product_name})
        return True
    else:
        return False


def get_item(product_name, field="name"):
    # pega um item especifico, pesquisando por um campo, por padrão o name
    if collection.find_one({field: product_name}):
        return collection.find_one({field: product_name})
    else:
        return False

def get_all_items(query=None):
    if query == None:
        # pega todos os itens da loja
        registers = list()
        for x in collection.find().sort("name", 1):
            registers.append(x)
    else:
        registers = list()
        for x in collection.find({"img": { "$regex": "^http" }}).sort("name", 1):
            registers.append(x)

    return registers

