# Funções uteis
import discord
import locale
from pytz import timezone
from datetime import datetime, timedelta
from capas.all_capas import lista_de_capas

locale.setlocale(locale.LC_ALL, '')

def get_prefix():
    return "k!"

def all_channels():
    # cassino, c4, games é diferente
    return [983428794637488148, 983462889086124072, 983428734692503652, 968045281843220520, 968048613806723082, 982711181259210833, 981554796358152202, 976973013293604925]
    #return [982321966268686407, 982321436469362778, 982321475996504084, 977271218757570611, 944649962686386256, 883810728140734506]

prefix = get_prefix()

def pass_to_money(value:int):
    # passa numeros 123456789 para 123.456.789
    new = "{:,d}".format(value)
    return new.replace(",", ".")

def pass_to_date(value):
    # passa inteiros 20220525 para str 25/05/2022
    if int(value) > 0:
        data = f'Até {str(value)[6:]}/{str(value)[4:6]}/{str(value)[:4]}'
    else:
        return '-'
    return data

def pass_to_num(value):
    try:
        num = int(value)
        return num
    except:
        return False


def get_id(member):
    # recebe um membro se for o Id já retorna se for <@member> remove os <@ > e retorna Id
    try:
        if "<@" in member:
            Id = member.replace("<@", "")
            member = Id.replace(">", "")
        return int(member)
    except: return False

def verify_role_or_id(msg):
    # recebe um cargo se for Id já retorna se for <@&ID> remove os <@& > e retorna Id
    try:
        if "<@&" in msg:
            Id = msg.replace("<@&", "")
            msg = Id.replace(">", "")
        return int(msg)
    except: return False

def remove_png(name):
    if ".png" in name:
        name = name.replace(".png", "")
    return name

def find_capa(name):
    # recebe uma string e procura na lista de capas se ela existe
    for x in lista_de_capas:
        if x[:8] in name:
            return(x)
    return False

def get_days(vip=0) -> int:
    # retorna o dia atual ou o dia que acaba o vip da pessoa
    now = datetime.now(timezone('America/Sao_Paulo'))
    if vip == 7:
        time = timedelta(days=7)
        now += time
    elif vip == 15:
        time = timedelta(days=15)
        now += time
    elif vip == 30:
        time = timedelta(days=30)
        now += time 
    now = str(now) 
    data = int(now.replace("-", "")[:8])
    return data

def pass_to_dict(response:str):
    """passa uma string para dicionário"""
    lista = response.split()
    dkey = (lista[0]).replace(":", "")
    dvalue = ' '.join(lista[1:])
    if dkey == "price":
        return dkey, int(dvalue)
    elif dkey == "role":
        try:
            int(dvalue)
            value = dvalue
            return dkey, value
        except:
            value = dvalue.replace("<@&", "")
            value = value.replace(">", "")
            return dkey, value
    return dkey, dvalue.lower()

