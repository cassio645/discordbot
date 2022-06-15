from pymongo import MongoClient
from decouple import config


MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Evento"]
collection = db["premios"]


def add_premio(dados):
    if collection.insert_many(dados):
        print("foi")
    else:
        print("nao deu")


def get_premio(product_name):
    if collection.find_one({"name": product_name}):
        return collection.find_one({"name": product_name})
    else:
        return False

def edit_premio(product_name, chave, valor):
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