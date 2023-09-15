from typing import Tuple, Union
from datetime import datetime, timedelta
from pymongo import MongoClient
from decouple import config


MONGO_TOKEN = config("MONGO_TOKEN")

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["cooldown"]

prefix = get_prefix()


def new_user_cooldown(
    user_id: int, guess_limit: int = 0, aposta_limit: int = 0
) -> None:
    """
    Registra um novo usuário para o cooldown de apostas do bot.

    Args:
        user_id (int): O ID do usuário a ser registrado.
        guess_limit (int, optional): O limite de tempo (em segundos) entre palpites (padrão: 0).
        aposta_limit (int, optional): O limite de tempo (em segundos) entre apostas (padrão: 0).
    """
    hora = datetime.now()
    dados = {
        "_id": user_id,
        "guess_time": hora,
        "guess_limit": guess_limit,
        "aposta_time": hora,
        "aposta_limit": aposta_limit,
    }
    collection.insert_one(dados)


def add_limit(user_id: int) -> bool:
    """
    Adiciona um limite de apostas para um usuário no cooldown de apostas do bot.

    Esta função controla o limite de apostas de um usuário e atualiza o tempo de cooldown.

    Args:
        user_id (int): O ID do usuário para o qual o limite de apostas será adicionado.

    Returns:
        bool: True se o limite de apostas foi adicionado com sucesso, False se o usuário já atingiu o limite máximo.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["guess_limit"] < 5:
            cd = user["guess_time"] + timedelta(hours=1)
            if cd <= datetime.now():
                newvalues = {"$set": {"guess_time": datetime.now(), "guess_limit": 1}}
                collection.update_one(user, newvalues)
                return True
            limit = user["guess_limit"] + 1
            newvalues = {"$set": {"guess_time": datetime.now(), "guess_limit": limit}}
            collection.update_one(user, newvalues)
            return True
        else:
            return check_guess_cooldown(user_id)
    else:
        new_user_cooldown(user_id, guess_limit=1)
        return True


def check_guess_cooldown(user_id: int) -> Union[bool, str]:
    """
    Verifica o cooldown de apostas de um usuário.

    Esta função verifica se o usuário ainda está em cooldown após uma aposta e retorna
    o tempo restante até o fim do cooldown ou True se o cooldown expirou.

    Args:
        user_id (int): O ID do usuário para verificar o cooldown de apostas.

    Returns:
        Union[bool, str]: Se o cooldown ainda estiver ativo, retorna o tempo restante em formato de string (hh:mm:ss).
        Se o cooldown expirou, retorna True. Se o usuário não estiver registrado, retorna False.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["guess_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            newvalues = {"$set": {"guess_time": datetime.now(), "guess_limit": 1}}
            collection.update_one(user, newvalues)
            return True
        else:
            return str(cd - datetime.now())[2:7]
    else:
        return False


# cooldown aposta
def add_aposta(user_id: int) -> bool:
    """
    Adiciona um limite de apostas para um usuário no cooldown de apostas do bot.

    Esta função controla o limite de apostas de um usuário e atualiza o tempo de cooldown.

    Args:
        user_id (int): O ID do usuário para o qual o limite de apostas será adicionado.

    Returns:
        bool: True se o limite de apostas foi adicionado com sucesso, False se o usuário já atingiu o limite máximo.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["aposta_limit"] < 5:
            cd = user["aposta_time"] + timedelta(hours=1)
            if cd <= datetime.now():
                newvalues = {"$set": {"aposta_time": datetime.now(), "aposta_limit": 1}}
                collection.update_one(user, newvalues)
                return True
            limit = user["aposta_limit"] + 1
            newvalues = {"$set": {"aposta_time": datetime.now(), "aposta_limit": limit}}
            collection.update_one(user, newvalues)
            return True
        else:
            return check_aposta_cooldown(user_id)
    else:
        new_user_cooldown(user_id, aposta_limit=1)
        return True


def check_aposta_cooldown(user_id: int) -> Union[bool, str]:
    """
    Verifica o cooldown de apostas de um usuário.

    Esta função verifica se o usuário ainda está em cooldown após uma aposta e retorna
    o tempo restante até o fim do cooldown ou True se o cooldown expirou.

    Args:
        user_id (int): O ID do usuário para verificar o cooldown de apostas.

    Returns:
        Union[bool, str]: Se o cooldown ainda estiver ativo, retorna o tempo restante em formato de string (hh:mm:ss).
        Se o cooldown expirou, retorna True. Se o usuário não estiver registrado, retorna False.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["aposta_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            newvalues = {"$set": {"aposta_time": datetime.now(), "aposta_limit": 1}}
            collection.update_one(user, newvalues)
            return True
        else:
            return str(cd - datetime.now())[2:7]


def get_cooldown_guess(user_id: int) -> Tuple[int, Union[str, int]]:
    """
    Obtém informações sobre o cooldown de palpites de um usuário.

    Esta função retorna o limite de tempo de cooldown de palpites de um usuário e o tempo restante
    até o fim do cooldown.

    Args:
        user_id (int): O ID do usuário para obter informações sobre o cooldown de palpites.

    Returns:
        Tuple[int, Union[str, int]]: Um tuple contendo o limite de tempo de cooldown (em segundos) e o
        tempo restante até o fim do cooldown em formato de string (hh:mm:ss) ou 0 se o cooldown expirou.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["guess_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            return 0, 0
        else:
            return user["guess_limit"], str(cd - datetime.now())[2:7]
    else:
        return 0, 0


def get_cooldown_aposta(user_id: int) -> Tuple[int, Union[str, int]]:
    """
    Obtém informações sobre o cooldown de apostas de um usuário.

    Esta função retorna o limite de tempo de cooldown de apostas de um usuário e o tempo restante
    até o fim do cooldown.

    Args:
        user_id (int): O ID do usuário para obter informações sobre o cooldown de apostas.

    Returns:
        Tuple[int, Union[str, int]]: Um tuple contendo o limite de tempo de cooldown (em segundos) e o
        tempo restante até o fim do cooldown em formato de string (hh:mm:ss) ou 0 se o cooldown expirou.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["aposta_time"] + timedelta(hours=1)
        if cd <= datetime.now():
            return 0, 0
        else:
            return user["aposta_limit"], str(cd - datetime.now())[2:7]
    else:
        return 0, 0
