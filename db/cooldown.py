from pytz import timezone
from datetime import datetime, timedelta
from pymongo import MongoClient
from decouple import config
from pymongo.errors import DuplicateKeyError
from code.funcoes import get_prefix, get_days, find_capa


MONGO_TOKEN = config('MONGO_TOKEN')

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Discord"]
collection = db["cooldown"]

prefix = get_prefix()

def new_user_cooldown(user_id, guess_time=0, guess_limit=0, aposta_time=0, aposta_limit=0):
    dados = {"_id": user_id, "guess_time": guess_time, "guess_limit": guess_limit, "aposta_time": aposta_time, "aposta_limit": aposta_limit}
    collection.insert_one(dados)


def add_limit(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["guess_limit"] < 5:
            if user["guess_time"] == 0:
                newvalues = { "$set": { "guess_time":  datetime.now(), "guess_limit": 1} }
                collection.update_one(user, newvalues)
                return True
            cd = user["guess_time"] + timedelta(hours=1)
            if cd < datetime.now():
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
        new_user_cooldown(user_id, guess_time=datetime.now(), guess_limit=1)
        return True


def check_guess_cooldown(user_id):
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["guess_time"] + timedelta(hours=1)
        if cd < datetime.now():
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
            if user["aposta_time"] == 0:
                newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": 1} }
                collection.update_one(user, newvalues)
                return True
            cd = user["aposta_time"] + timedelta(hours=1)
            if cd < datetime.now():
                newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": 1} }
                collection.update_one(user, newvalues)
                return True 
            limit = user["aposta_limit"] + 1
            newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": limit} }
            collection.update_one(user, newvalues)
            return True
        else:
            return check_guess_cooldown(user_id)
    else:
        new_user_cooldown(user_id, aposta_time=datetime.now(), aposta_limit=1)
        return True          


def check_aposta_cooldown(user_id):
    user = collection.find_one({"_id": user_id})
    cd = user["aposta_time"] + timedelta(hours=1)
    if cd < datetime.now():
        newvalues = { "$set": { "aposta_time":  datetime.now(), "aposta_limit": 1} }
        collection.update_one(user, newvalues)
        return True
    else:
        return str(cd - datetime.now())[2:7]
