import math

mocnenec = input("Zadejte algebrogram pro mocněnce: ").lower().strip()
vysledek = input("Zadejte algebrogram pro výsledek: ").lower().strip()

def algorithm(num):
    str1 = f"{mocnenec}{vysledek}"
    str2 = f"{num}{num*num}"
    for i in range(len(str1)):
        if not str1[i].isdecimal():
            if str2[i] in str1: return False
            str1 = str1.replace(str1[i], str2[i])
    if str1 != str2: return False
    return True

for i in range(int(math.sqrt(10 ** (len(vysledek) - 1))), 10 ** len(mocnenec)):
    if algorithm(i):
        print(i)
