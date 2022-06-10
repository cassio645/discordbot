from pytz import timezone
from datetime import datetime, timedelta
from pymongo import MongoClient
from decouple import config
from pymongo.errors import DuplicateKeyError
from code.funcoes import get_prefix, get_days, find_capa


MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["cooldown"]

prefix = get_prefix()

def new_user_cooldown(user_id, guess_limit=0, aposta_limit=0):
    hora = datetime.now()
    dados = {"_id": user_id, "guess_time": hora, "guess_limit": guess_limit, "aposta_time": hora, "aposta_limit": aposta_limit}
    collection.insert_one(dados)


def add_limit(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["guess_limit"] < 5:
            cd = user["guess_time"] + timedelta(hours=1)
            if cd <= datetime.now():
                newvalues = { "$set": { "guess_time":  datetime.now(), "guess_limit": 1} }
                collection.update_one(user, newvalues)
                return True 
            limit = user["guess_limit"] + 1
            newvalues = { "$set": { "guess_time":  datetime.now(), "guess_limit": limit} }
            collection.update_one(user, newvalues)
            return True
        else:
            return check_guess_cooldown(user_id)
    else:
        new_user_cooldown(user_id, guess_limit=1)
        return True


def check_guess_cooldown(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["guess_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            newvalues = { "$set": { "guess_time":  datetime.now(), "guess_limit": 1} }
            collection.update_one(user, newvalues)
            return True
        else:
            return str(cd - datetime.now())[2:7]

# cooldown aposta

def add_aposta(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["aposta_limit"] < 5:
            cd = user["aposta_time"] + timedelta(hours=1)
            if cd <= datetime.now():
                newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": 1} }
                collection.update_one(user, newvalues)
                return True 
            limit = user["aposta_limit"] + 1
            newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": limit} }
            collection.update_one(user, newvalues)
            return True
        else:
            return check_aposta_cooldown(user_id)
    else:
        new_user_cooldown(user_id, aposta_limit=1)
        return True         


def check_aposta_cooldown(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["aposta_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": 1} }
            collection.update_one(user, newvalues)
            return True
        else:
            return str(cd - datetime.now())[2:7]


def get_cooldown_guess(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["guess_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            return 0, 0
        else:
            return user["guess_limit"], str(cd - datetime.now())[2:7]
    else:
        return 0, 0


def get_cooldown_aposta(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["aposta_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            return 0, 0
        else:
            return user["aposta_limit"], str(cd - datetime.now())[2:7]
    else:
        return 0, 0

