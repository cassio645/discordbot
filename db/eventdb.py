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


def add_milho_users(users, milho=1):
    lista_users = []
    for user in users:
        lista_users.append(user.id)
    for x in collection.find({"_id": {"$gt": 0}}):
        if x["_id"] in lista_users:
            total = milho + x["milho"]
            new_values = { "$set": { "milho":  total} }
            collection.update_one(x, new_values)
            lista_users.remove(x["_id"])
    if lista_users:
        lista_de_novos_users = []
        for user in lista_users:
            lista_de_novos_users.append({"_id": user, "milho": 1, "premios": []})
        collection.insert_many(lista_de_novos_users)
        
            
def add_milho(user_id, milho=1):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        total = user["milho"] + milho
        new_values = { "$set": { "milho":  total} }
        collection.update_one(user, new_values)
    else:
        add_new_user_event(user_id, milho=milho)
        


def get_milho(user_id):
    # pega o valor de milho da pessoa
    try:
        user = collection.find_one({"_id": user_id})
        milho = user["milho"]
        return milho
    except TypeError:
        return 0

