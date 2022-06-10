from pytz import timezone
from datetime import datetime, timedelta
from pymongo import MongoClient
from decouple import config
from pymongo.errors import DuplicateKeyError
from code.funcoes import get_prefix, get_days, find_capa, find_cor


MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["users"]

prefix = get_prefix()

# --------------- Adiciona um novo usuário ----------------
def add_new_user(user_id, money=0, c4=0, vip=0, daily=0, rep=0, cdrep=0, status=None, cor=None):
    user_capas = ["default"]
    cores = []
    if cor:
        cores[cor]
    if status == None:
        status = f"Use {prefix}status <frase> para alterar aqui..."
    dados = {"_id": user_id, "money": money, "c4": c4, "vip": vip, "daily": daily, "rep": rep, "cdrep": cdrep, "status": status, "user_capas": user_capas, "capa": "default.png", "user_cores": cores}
    collection.insert_one(dados)




# ----------- Funções para USER ------------------
def get_user(user_id):
    # pega infos de um usuário
    try:
        user = collection.find_one({"_id": user_id})
        return user
    except:
        return False

def get_time_rep_and_add(user_id):
    """ verifica se passou 1h desde a ultima rep, se a pessoa nunca deu rep "0" ou n tem perfilfica com a hr atual e retorna True. Se ainda nao passou 1h retorna o tempo que falta.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["cdrep"] == 0:
            now = datetime.now() + timedelta(hours=1)
            newvalues = { "$set": { "cdrep":  now} }
            collection.update_one(user, newvalues)
            return True
        cd = user["cdrep"]
        if cd <= datetime.now():
            now = datetime.now() + timedelta(hours=1)
            newvalues = { "$set": { "cdrep":  now} }
            collection.update_one(user, newvalues)
            return True
        return str(cd - datetime.now())[2:7]
    else:
        add_new_user(user_id, cdrep=datetime.now())
        return True

def get_time_rep(user_id):
    #apenas pega o tempo de rep
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["cdrep"]
        if user["cdrep"] == 0 or (cd <= datetime.now()):
            return True
        return str(cd - datetime.now())[2:7]
    else:
        return True


def add_rep(user_id):
    # adiciona mais 1 no numero de rep da pessoa, se ela n tem perfil cria com 1 rep
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        newrep = (user["rep"]) + 1
        newvalues = { "$set": {"rep": newrep}}
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, rep=1)

def get_user_cores(user_id):
    # pega a lista de capas de um usuário
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        return user["user_cores"]
    return False

def get_user_capas(user_id):
    # pega a lista de capas de um usuário
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        return user["user_capas"]
    return False

def set_cor(user_id, cor):
    # seleciona a cor que ele quer usar
    user = collection.find_one({"_id": user_id})
    newvalues = { "$set": { "cor":  cor} }
    collection.update_one(user, newvalues)

def set_capa(user_id, capa):
    # seleciona a capa que ele quer usar
    user = collection.find_one({"_id": user_id})
    newvalues = { "$set": { "capa":  capa} }
    collection.update_one(user, newvalues)


def add_cor(user_id, cor):
    # adiciona uma cor na lista de cores do user
    user = collection.find_one({"_id": user_id})
    cor = find_cor(cor)
    if cor:
        collection.update_one(user, {"$push": {"user_cores": cor}})
        return True
    else:
        return "Cor não encontrada."


def add_capa(user_id, capa):
    # adiciona uma nova capa na lista de capas do usuário
    user = collection.find_one({"_id": user_id})
    capa = find_capa(capa)
    print(f"no db: {capa}")
    if capa:
        collection.update_one(user,{"$push": {"user_capas": capa}})
        return True
    else:
        return "Capa não encontrada."

def set_status(user_id, status):
    # recebe uma frase e a deixa como status daquele usuario
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id}) 
        newvalues = { "$set": { "status":  status} }
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, status=status)

# ---------- Funções de Vip ------------
def insert_vip(user_id, time_vip):
    # insere vip e o tempo de vip
    time = get_days(vip=time_vip)
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id}) 
        newvalues = { "$set": { "vip":  time} }
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, vip=time)

def get_all_vip():
    # pega uma lista de todos usuarios que são vip
	registers = list()
	for x in collection.find({"vip": {"$gt": 0}}):
		registers.append(x)
	return registers

def get_vip(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["vip"] > 0:
            return True
        else: return False
    return False

def end_vip(user_id):
    # finaliza o vip de um usuario
    user = collection.find_one({"_id": user_id}) 
    newvalues = { "$set": { "vip":  0} }
    collection.update_one(user, newvalues)


# ----------- Funções de C4  -------------
def insert_c4_winner(user_id):
    # adiciona uma vitoria
    c4_update = 1
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        vitorias = user["c4"]
        vitorias += c4_update
        newvalues = { "$set": { "c4":  vitorias} }
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, c4=c4_update)


# ------------ Funções de Money ---------------
def add_money(user_id, values):
    # adiciona kivs
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        total = values + user["money"]
        new_values = { "$set": { "money":  total} }
        collection.update_one(user, new_values)
    else:
        add_new_user(user_id, money=values)

def remove_money(user_id, values):
    # remove uma quantia de kivs, se a quantia for maior q a pessoa tem, retorna False
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if values > user["money"]:
            return False
        else:
            total = user["money"] - values
            new_values = { "$set": { "money":  total} }
            collection.update_one(user, new_values)
            return True
    else: return False

def get_balance(user_id):
    # pega o valor de kivs da pessoa
    try:
        user = collection.find_one({"_id": user_id})
        kivs = user["money"]
        return kivs
    except TypeError:
        return 0


# ---------- Funções de Daily ---------------------
def get_daily(user_id):
    # pega a hr do ultimo daily
    try:
        user = collection.find_one({"_id": user_id})
        data = user["daily"]
        return data
    except TypeError:
        return 0


def add_daily(user_id, money, daily):
    # adiciona o cooldown do daily
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        total = user["money"] + money
        new_values = { "$set": { "money":  total, "daily": daily} }
        collection.update_one(user, new_values)
    else:
        add_new_user(user_id, money=money, daily=daily)

# ---------- rank money, c4, rep ------------------
def get_rank(query):
    # consulta o rank por completo e ordena pela ordem de money
    registers = list()
    for x in collection.find({query: {"$gt": 0}}):
        registers.append(x)
    ordered = (sorted(registers, key = lambda i: i[query],reverse=True))
    return ordered


# -------- DELETA todos os dados do usuário ----------
def delete_data(user_id):
	# apaga os dados de um usuário
	try:
		collection.delete_one({"_id": user_id})
	except:
		pass

"""
def add_new_field():
    novo = {"user_cores": []}

    myquery = { "_id": { "$gt": 0} }
    newvalues = { "$set":  novo}
    collection.update_many(myquery, newvalues)
    return True

"""