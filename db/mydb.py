from datetime import datetime, timedelta
from typing import Union
from pymongo import MongoClient
from decouple import config
from code.funcoes import get_prefix, get_days, find_capa, find_cor

MONGO_TOKEN = config("MONGO_TOKEN")

cluster = MongoClient(MONGO_TOKEN)
db = cluster["Kivida"]
collection = db["users"]

prefix = get_prefix()


def add_new_user(
    user_id: int, money=0, c4=0, vip=0, daily=0, rep=0, cdrep=0, status=None, cor=None
) -> None:
    """
    Adiciona um novo usuário ao banco de dados.

    Args:
        user_id (int): O ID do usuário a ser adicionado.
        money (int, optional): A quantidade de dinheiro do usuário. Defaults to 0.
        c4 (int, optional): A quantidade de c4 do usuário. Defaults to 0.
        vip (int, optional): O status VIP do usuário. Defaults to 0.
        daily (int, optional): A última vez que o usuário coletou a recompensa diária. Defaults to 0.
        rep (int, optional): A reputação do usuário. Defaults to 0.
        cdrep (int, optional): O cooldown da reputação do usuário. Defaults to 0.
        status (str, optional): O status do usuário. Defaults to None.
        cor (str, optional): A cor do usuário. Defaults to None.
    """
    user_capas = ["default"]
    cores = []
    if cor:
        cores[cor]
    if status is None:
        status = f"Use {prefix}status <frase> para alterar aqui..."
    dados = {
        "_id": user_id,
        "money": money,
        "c4": c4,
        "vip": vip,
        "daily": daily,
        "rep": rep,
        "cdrep": cdrep,
        "status": status,
        "user_capas": user_capas,
        "capa": "default.png",
        "user_cores": cores,
    }
    collection.insert_one(dados)


def get_user(user_id: int):
    """
    Obtém informações de um usuário a partir do seu ID.

    Args:
        user_id (int): O ID do usuário a ser pesquisado.

    Returns:
        dict: Um dicionário contendo informações do usuário, ou False se o usuário não for encontrado.
    """
    try:
        user = collection.find_one({"_id": user_id})
        return user
    except:
        return False


def get_time_rep_and_add(user_id: int) -> Union[bool, str]:
    """
    Verifica se passou 1 hora desde a última reputação (rep) concedida. Se o usuário nunca deu rep ("cdrep" igual a 0) ou não tem um perfil,
    a função atualiza o tempo de "cdrep" com a hora atual e retorna True. Caso contrário, a função retorna o tempo restante até que o usuário
    possa dar rep novamente.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        Union[bool, str]: Retorna True se o usuário pode dar rep agora ou uma string que representa o tempo restante (no formato "hh:mm:ss").
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["cdrep"] == 0:
            now = datetime.now() + timedelta(hours=1)
            newvalues = {"$set": {"cdrep": now}}
            collection.update_one(user, newvalues)
            return True
        cd = user["cdrep"]
        if cd <= datetime.now():
            now = datetime.now() + timedelta(hours=1)
            newvalues = {"$set": {"cdrep": now}}
            collection.update_one(user, newvalues)
            return True
        return str(cd - datetime.now())[2:7]
    else:
        add_new_user(user_id, cdrep=datetime.now())
        return True


def get_time_rep(user_id: int) -> Union[bool, str]:
    """
    Obtém o tempo restante até que o usuário possa dar reputação (rep) novamente.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        Union[bool, str]: Retorna True se o usuário pode dar rep agora ou uma string que representa o tempo restante (no formato "hh:mm:ss").
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        cd = user["cdrep"]
        if user["cdrep"] == 0 or (cd <= datetime.now()):
            return True
        return str(cd - datetime.now())[2:7]
    else:
        return True


def add_rep(user_id: int) -> None:
    """
    Adiciona 1 ao número de reputação (rep) de um usuário. Se o usuário não tiver um perfil, cria um com 1 rep.

    Args:
        user_id (int): O ID do usuário.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        newrep = (user["rep"]) + 1
        newvalues = {"$set": {"rep": newrep}}
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, rep=1)


def get_user_cores(user_id: int) -> Union[list, bool]:
    """
    Obtém a lista de cores de um usuário.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        Union[list, bool]: Uma lista de cores se o usuário tiver cores definidas ou False se o usuário não for encontrado.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        return user["user_cores"]
    return False


def get_user_capas(user_id: int) -> Union[list, bool]:
    """
    Obtém a lista de capas de um usuário.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        Union[list, bool]: Uma lista de capas se o usuário tiver capas definidas ou False se o usuário não for encontrado.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        return user["user_capas"]
    return False


def set_cor(user_id: int, cor: str) -> None:
    """
    Define a cor que um usuário deseja usar.

    Args:
        user_id (int): O ID do usuário.
        cor (str): A cor que o usuário deseja definir.
    """
    user = collection.find_one({"_id": user_id})
    newvalues = {"$set": {"cor": cor}}
    collection.update_one(user, newvalues)


def set_capa(user_id: int, capa: str) -> None:
    """
    Define a capa que um usuário deseja usar.

    Args:
        user_id (int): O ID do usuário.
        capa (str): A capa que o usuário deseja definir.
    """
    user = collection.find_one({"_id": user_id})
    newvalues = {"$set": {"capa": capa}}
    collection.update_one(user, newvalues)


def add_cor(user_id: int, cor: str) -> Union[bool, str]:
    """
    Adiciona uma cor à lista de cores do usuário.

    Args:
        user_id (int): O ID do usuário.
        cor (str): A cor a ser adicionada à lista de cores.

    Returns:
        Union[bool, str]: True se a cor foi adicionada com sucesso, ou uma string de erro se a cor não foi encontrada.
    """
    user = collection.find_one({"_id": user_id})
    cor = find_cor(cor)
    if cor:
        collection.update_one(user, {"$push": {"user_cores": cor}})
        return True
    else:
        return "Cor não encontrada."


def add_capa(user_id: int, capa: str) -> Union[bool, str]:
    """
    Adiciona uma nova capa à lista de capas do usuário.

    Args:
        user_id (int): O ID do usuário.
        capa (str): A capa a ser adicionada à lista de capas.

    Returns:
        Union[bool, str]: True se a capa foi adicionada com sucesso, ou uma string de erro se a capa não foi encontrada.
    """
    user = collection.find_one({"_id": user_id})
    capa = find_capa(capa)
    if capa:
        collection.update_one(user, {"$push": {"user_capas": capa}})
        return True
    else:
        return "Capa não encontrada."


def set_status(user_id: int, status: str) -> None:
    """
    Define uma frase como o status do usuário.

    Args:
        user_id (int): O ID do usuário.
        status (str): A frase a ser definida como status do usuário.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        newvalues = {"$set": {"status": status}}
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, status=status)


# ---------- Funções de Vip ------------
def insert_vip(user_id, time_vip: int) -> None:
    """
    Insere a condição VIP e o tempo de VIP para um usuário.

    Args:
        user_id (int): O ID do usuário.
        time_vip (int): O tempo de VIP em dias.

    Note:
        A função `get_days` é usada para calcular o tempo em dias com base no número de dias de VIP fornecido.
    """
    time = get_days(vip=time_vip)
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        newvalues = {"$set": {"vip": time}}
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, vip=time)


def get_all_vip() -> list:
    """
    Obtém uma lista de todos os usuários que possuem status VIP.

    Returns:
        list: Uma lista de registros de usuários VIP.
    """
    registers = list()
    for x in collection.find({"vip": {"$gt": 0}}):
        registers.append(x)
    return registers


def get_vip(user_id: int) -> bool:
    """
    Verifica se um usuário é VIP.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        bool: True se o usuário é VIP, False se não é VIP ou não foi encontrado.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if user["vip"] > 0:
            return True
    return False


def end_vip(user_id: int) -> None:
    """
    Finaliza o status VIP de um usuário, definindo-o como 0.

    Args:
        user_id (int): O ID do usuário cujo status VIP será encerrado.
    """
    user = collection.find_one({"_id": user_id})
    newvalues = {"$set": {"vip": 0}}
    collection.update_one(user, newvalues)


# ----------- Funções de C4  -------------
def insert_c4_winner(user_id: int) -> None:
    """
    Adiciona uma vitória ao contador de vitórias do usuário no jogo C4 (Connect Four).

    Args:
        user_id (int): O ID do usuário que venceu uma partida no jogo C4.
    """
    c4_update = 1
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        vitorias = user["c4"]
        vitorias += c4_update
        newvalues = {"$set": {"c4": vitorias}}
        collection.update_one(user, newvalues)
    else:
        add_new_user(user_id, c4=c4_update)


# ------------ Funções de Money ---------------
def add_money(user_id, values) -> None:
    """
    Adiciona uma quantidade de kivs à conta de um usuário.

    Args:
        user_id (int): O ID do usuário.
        values (int): A quantidade de kivs a ser adicionada.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        total = values + user["money"]
        new_values = {"$set": {"money": total}}
        collection.update_one(user, new_values)
    else:
        add_new_user(user_id, money=values)


def remove_money(user_id, values) -> bool:
    """
    Remove uma quantidade de kivs da conta de um usuário, se a quantidade for maior do que o usuário tem, retorna False.

    Args:
        user_id (int): O ID do usuário.
        values (int): A quantidade de kivs a ser removida.

    Returns:
        bool: True se a quantidade de kivs foi removida com sucesso, False se o usuário não tiver kivs suficientes.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        if values > user["money"]:
            return False
        else:
            total = user["money"] - values
            new_values = {"$set": {"money": total}}
            collection.update_one(user, new_values)
            return True
    else:
        return False


def get_balance(user_id: int) -> int:
    """
    Obtém o saldo de kivs de um usuário.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        int: O saldo de kivs do usuário ou 0 se o usuário não for encontrado.
    """
    try:
        user = collection.find_one({"_id": user_id})
        kivs = user["money"]
        return kivs
    except TypeError:
        return 0


# ---------- Funções de Daily ---------------------
def get_daily(user_id: int) -> int:
    """
    Obtém a data (hora) do último daily de um usuário.

    Args:
        user_id (int): O ID do usuário.

    Returns:
        int: A data (hora) do último daily do usuário ou 0 se o usuário não for encontrado.
    """
    try:
        user = collection.find_one({"_id": user_id})
        data = user["daily"]  # Data vem formatada como int
        return data
    except TypeError:
        return 0


def add_daily(user_id: int, money: int, daily: int) -> None:
    """
    Adiciona o cooldown do daily e uma quantidade de dinheiro à conta de um usuário.

    Args:
        user_id (int): O ID do usuário.
        money (int): A quantidade de dinheiro a ser adicionada à conta do usuário.
        daily (int): O novo valor do cooldown do daily para o usuário.
    """
    if collection.find_one({"_id": user_id}):
        user = collection.find_one({"_id": user_id})
        total = user["money"] + money
        new_values = {"$set": {"money": total, "daily": daily}}
        collection.update_one(user, new_values)
    else:
        add_new_user(user_id, money=money, daily=daily)


# ---------- rank money, c4, rep ------------------
def get_rank(query: str) -> list:
    """
    Consulta o ranking completo de uma métrica específica (money, c4 ou rep) e ordena em ordem decrescente dessa métrica.

    Args:
        query (str): A métrica pela qual o ranking deve ser consultado (money, c4 ou rep).

    Returns:
        list: Uma lista de registros de usuários ordenados pela métrica especificada em ordem decrescente.
    """
    registers = list()
    for x in collection.find({query: {"$gt": 0}}):
        registers.append(x)
    ordered = sorted(registers, key=lambda i: i[query], reverse=True)
    return ordered


# -------- DELETA todos os dados do usuário ----------
def delete_data(user_id: int) -> None:
    """
    Apaga os dados de um usuário.

    Args:
        user_id (int): O ID do usuário cujos dados devem ser excluídos.
    """
    try:
        collection.delete_one({"_id": user_id})
    except:
        pass
