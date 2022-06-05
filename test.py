from random import randint

a_letra = ""
a_ganhou = 0

letra = ""
ganhou = 0

for _ in range(10000):
    n = randint(1, 100)
    if n == 1:
        a_letra += "1"
        a_ganhou += 1
    elif n < 4:
        a_letra += "2"
        a_ganhou += 1
    elif n < 7:
        a_letra += "3"
        a_ganhou += 1
    elif n < 11:
        a_letra += "4"
        a_ganhou += 1
    elif n < 16:
        a_letra += "5"
        a_ganhou += 1

for _ in range(10000):
    n = randint(1, 1000)
    if n < 4:
        letra += "1"
        ganhou += 1
    elif n < 15:
        letra += "2"
        ganhou += 1
    elif n < 35:
        letra += "3"
        ganhou += 1
    elif n < 65:
        letra += "4"
        ganhou += 1
    elif n < 120:
        letra += "5"
        ganhou += 1



print(f"Ganhou antigo {a_ganhou} | Ganhou novo {ganhou}\n1: {a_letra.count('1')} | {letra.count('1')}\n2: {a_letra.count('2')} | {letra.count('2')}\n3: {a_letra.count('3')} | {letra.count('3')}\n4: {a_letra.count('4')} | {letra.count('4')}\n5: {a_letra.count('5')} | {letra.count('5')}")

