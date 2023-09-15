# Funções uteis
from typing import Any, List, Union
import locale
from pytz import timezone
from datetime import datetime, timedelta
from capas.all_capas import lista_de_capas

locale.setlocale(locale.LC_ALL, "")


def get_prefix() -> str:
    """
    Retorna o prefixo padrão usado para invocar comandos.

    Returns:
        str: O prefixo padrão.
    """
    return "k!"


def all_channels() -> List[int]:
    """
    Retorna uma lista de IDs de canais específicos.

    Returns:
        List[int]: Uma lista de IDs de canais.
    """
    return []  # Lista de canais


prefix = get_prefix()


def pass_to_money(value: int) -> str:
    """
    Formata um número inteiro como uma string representando uma quantia em dinheiro
    com separadores de milhares (ponto).

    Args:
        value (int): O valor inteiro a ser formatado.

    Returns:
        str: Uma string formatada representando a quantia em dinheiro.
    """
    # Esta função formata um número inteiro como uma string representando uma quantia em dinheiro,
    # inserindo separadores de milhares (pontos) para melhor legibilidade.
    new = "{:,d}".format(value)
    return new.replace(",", ".")


def pass_to_date(value: int) -> str:
    """
    Formata um número inteiro como uma string representando uma data no formato 'dd/mm/yyyy'.

    Args:
        value (int): O valor inteiro a ser formatado como data (ex: 20220525).

    Returns:
        str: Uma string formatada representando a data no formato 'dd/mm/yyyy' (ex: '25/05/2022').
             Retorna '-' se o valor for menor ou igual a zero.
    """
    # Esta função formata um número inteiro como uma string representando uma data no formato 'dd/mm/yyyy'.
    # Ela espera um valor no formato 'aaaammdd' e o converte para 'dd/mm/yyyy'.
    if int(value) > 0:
        data = f"{str(value)[6:]}/{str(value)[4:6]}/{str(value)[:4]}"
    else:
        return "-"
    return data


def pass_to_num(value: Any) -> Union[int, bool]:
    """
    Converte um valor para um número inteiro.

    Args:
        value (Any): O valor a ser convertido.

    Returns:
        Union[int, bool]: Um número inteiro se a conversão for bem-sucedida, caso contrário, retorna False.
    """
    try:
        num = int(value)
        return num
    except ValueError:
        return False


def get_id(member: Union[str, int]) -> Union[int, bool]:
    """
    Obtém o ID de um membro.

    Args:
        member (str ou int): O ID do membro ou uma representação de menção "<@member>".

    Returns:
        int ou bool: O ID do membro (int) se for um valor válido, False (bool) caso contrário.
    """
    try:
        if "<@" in member:
            Id = member.replace("<@", "")
            member = Id.replace(">", "")
        return int(member)
    except:
        return False


def verify_role_or_id(msg: str) -> Union[int, bool]:
    """
    Verifica e retorna um ID de cargo ou um valor numérico.

    Args:
        msg (str): A mensagem que contém o ID do cargo ou um valor numérico.

    Returns:
        Union[int, bool]: O ID do cargo como um número inteiro se for um cargo válido,
        caso contrário, retorna False.
    """
    try:
        if "<@&" in msg:
            role_id = msg.replace("<@&", "")
            msg = role_id.replace(">", "")
        return int(msg)
    except ValueError:
        return False


def remove_png(name: str) -> str:
    """
    Remove a extensão ".png" de uma string, se presente.

    Args:
        name (str): O nome ou caminho de arquivo que pode conter a extensão ".png".

    Returns:
        str: O nome ou caminho de arquivo sem a extensão ".png".
    """
    if ".png" in name:
        name = name.replace(".png", "")
    return name


def find_cor(name: str) -> Union[int, bool]:
    """
    Encontra o identificador (ID) da cor com base no nome ou ID fornecido.

    Args:
        name (str): O nome ou ID da cor, que pode estar no formato "@nome", "<&ID>", ou apenas o nome/ID.

    Returns:
        Union[int, bool]: O ID da cor encontrado. Caso contrário, retorna False.
    """
    if "@" in name:
        name = str(name.replace("@", ""))
        if "<&" in name:
            n = name.replace("<&", "")
            name = n.replace(">", "")
    if name.lower() in ["cor lizard", "lizard", "984796466579128330"]:
        return 984796466579128330
    elif name.lower() in ["cor ciano", "ciano", "984800368481435698"]:
        return 984800368481435698
    elif name.lower() in [
        "cor amethyst",
        "amethyst",
        "ametyst",
        "cor ametyst",
        "cor amethist",
        "amethist",
        "984797215715393546",
    ]:
        return 984797215715393546
    elif name.lower() in ["cor blue", "blue", "984796289541742614"]:
        return 984796289541742614
    elif name.lower() in [
        "cor pink",
        "cor pinky",
        "pink",
        "pinky",
        "984796216263065669",
    ]:
        return 984796216263065669
    elif name.lower() in ["cor amber", "amber", "984796054727852042"]:
        return 984796054727852042
    elif name.lower() in [
        "cor pantone",
        "cor panetone",
        "pantone",
        "panetone",
        "984796141952573440",
    ]:
        return 984796141952573440
    elif name.lower() in [
        "cor barbie",
        "barbie",
        "cor barbe",
        "barbe",
        "968053597952692264",
    ]:
        return 968053597952692264
    elif name.lower() in ["cor red", "red", "984796904573526026"]:
        return 984796904573526026
    elif name.lower() in ["cor crayola", "crayola", "984796377433407539"]:
        return 984796377433407539
    elif name.lower() in ["cor rosy", "rosy", "984797948405743657"]:
        return 984797948405743657
    elif name.lower() in [
        "cor powder",
        "powder",
        "cor power",
        "power",
        "984798122674913300",
    ]:
        return 984798122674913300
    elif name.lower() in ["cor cream", "cream", " 984798336039125072"]:
        return 984798336039125072
    elif name.lower() in [
        "cor celadon",
        "celadon",
        "cor celadom",
        "celadom",
        "984798521599352863",
    ]:
        return 984798521599352863
    elif name.lower() in [
        "cor black",
        "black",
        "preto",
        "cor preto",
        "preta",
        "cor preta",
        "985256011243868190",
    ]:
        return 985256011243868190
    else:
        return False


def find_capa(name: str) -> Union[str, bool]:
    """
    Encontra o nome de uma capa na lista de capas com base no nome fornecido.

    Args:
        name (str): O nome da capa a ser procurada, que pode incluir ou não a extensão ".png".

    Returns:
        Union[str, bool]: O nome da capa encontrado na lista, incluindo a extensão ".png", se for uma correspondência.
                          Caso contrário, retorna False.
    """
    # Adiciona a extensão ".png" à string fornecida
    name += ".png"

    # Verifica se o nome (com ou sem extensão) existe na lista de capas
    for x in lista_de_capas:
        if name in [x, x[:8]]:
            return x  # Retorna o nome da capa encontrado, incluindo ".png"

    # Retorna False se o nome da capa não foi encontrado na lista
    return False


def get_days(vip: int = 0) -> int:
    """
    Retorna o dia atual ou o dia em que o status VIP da pessoa acaba.

    Args:
        vip (int, optional): O período VIP da pessoa em dias (0 se não for VIP). Pode ser 7, 15 ou 30.
                            (Padrão: 0)

    Returns:
        int: O dia atual ou o dia em que o status VIP da pessoa acaba.
    """
    # Obtém a data e hora atuais na zona de fuso horário 'America/Sao_Paulo'
    now = datetime.now(timezone("America/Sao_Paulo"))

    # Se a pessoa for VIP, adiciona o período VIP aos dias atuais
    if vip == 7:
        time = timedelta(days=7)
        now += time
    elif vip == 15:
        time = timedelta(days=15)
        now += time
    elif vip == 30:
        time = timedelta(days=30)
        now += time

    # Converte a data e hora resultante em uma string e extrai os primeiros 8 caracteres
    now = str(now)
    data = int(now.replace("-", "")[:8])

    return data


def pass_to_dict(response: str) -> tuple:
    """
    Converte uma string em um par chave-valor em forma de tupla.

    Args:
        response (str): A string a ser convertida.

    Returns:
        tuple: Uma tupla contendo a chave (key) e o valor (value) extraídos da string.
    """
    # Divide a string em uma lista de palavras
    lista = response.split()

    # Remove os dois pontos ':' da chave
    dkey = lista[0].replace(":", "")

    # Reúne o restante da lista como o valor (value)
    dvalue = " ".join(lista[1:])

    # Verifica se a chave é "price" e converte o valor para inteiro
    if dkey == "price":
        return dkey, int(dvalue)

    # Verifica se a chave é "role" e tenta converter o valor para inteiro
    elif dkey == "role":
        try:
            value = int(dvalue)
            return dkey, value
        except:
            # Se não puder ser convertido para inteiro, remove os caracteres "<@&" e ">" do valor
            value = dvalue.replace("<@&", "").replace(">", "")
            return dkey, value

    # Se a chave não for "price" ou "role", converte o valor para letras minúsculas e retorna
    return dkey, dvalue.lower()
