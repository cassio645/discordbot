from pymongo import MongoClient
from decouple import config
from pymongo.errors import DuplicateKeyError
from code.funcoes import get_prefix

MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Evento"]
collection = db["milho"]


def add_new_user_event(user_id, milho=1):
    try:
        dados = {"_id": user_id, "milho": milho, "premios": []}
        collection.insert_one(dados)
    except DuplicateKeyError():
        return


def add_milho(users, milho=1):
    lista_u = []
    for user in users:
        lista_u.append(user.id)
    for x in collection.find({"_id": {"$gt": 0}}):
        if x["_id"] in lista_u:
            total = milho + x["milho"]
            new_values = { "$set": { "milho":  total} }
            collection.update_one(x, new_values)
            lista_u.remove(x["_id"])
    if lista_u:
        for user in lista_u:
            add_new_user_event(user)

        


def get_milho(user_id):
    # pega o valor de milho da pessoa
    try:
        user = collection.find_one({"_id": user_id})
        milho = user["milho"]
        return milho
    except TypeError:
        return 0

