# """
# DU)
# 1) Naprogramujte jakoukoli hru s kostkami/kartami pro alespoň dva
#    hráče, jeden z nich bude počítač.
# 2) Hra musí být dostatečně složitá a pro pro uchování hodů
#    bude používat seznamy. Příliš jednoduché hry budou vráceny
#    k přepracování.
# 3) Musí být zobrazena pravidla.
# 4) Hra po spuštění zobrazí jednoduché textové menu:

#    1) Zobraz pravidla
#    2) Hrát hru
#    3) Konec
#    Zadej svou volbu:

#    Po ukončení hry se program vrací do menu, nedojde k ukončení
#    aplikace!
# 5) Hody hráčů (člověka i počítače) musí proběhnout až po stisku
#    klávesy Enter!
#    Použijte tento příkaz, který v podstatě způsobí čekání programu,
#    dokud uživatel nestiskne Enter: input("Stiskni Enter...").
#    Snažte se o přehledné výpisy stavu hry - např. průběžné body
#    za kolo a také celkové od začátku hry.
# 6) Každý musí mít jinou hru! :)
# """
import random

# todo hraci + pc

class color:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    gray = "\u001b[38;2;87;85;85m"
    bold = "\u001b[1m"
    none = "\u001b[0m"

def clear_screen():
    import os
    if os.name == "nt":
        os.system("cls")
        return
    os.system("clear")

def menu():
    clear_screen()
    volba = int(input("""Vítejte v PyUnu\n
1) Zobraz pravidla
2) Hrát hru
3) Konec\n
Zadej svou volbu: """))

    if volba == 1:
        pravidla()
    elif volba == 2:
        hra()
    elif volba == 3:
        return
    else:
        print("Neplatná volba, musí být číslo od 1 do 3")
        menu()

balicek = []
stul = []
hraci = {}
plus_card_buffer = []
log = []
current_player = ""
stopped = False
smer = 1
index = -1

def hra():
    clear_screen()

    global deck
    balicek = vygeneruj_karty()

    global players
    for i in range(verfify_input("Zadejte počet hráčů: ")):
        hraci.update({f"Hráč #{i + 1}": []})
        vzit_z_balicku(7, hraci[f"Hráč #{i + 1}"])
    for i in range(verfify_input("Zadejte počet PC: ")):
        hraci.update({f"PC #{i + 1}": []})
        vzit_z_balicku(7, hraci[f"PC #{i + 1}"])

    global log
    log = []

    global stul
    stul += vzit_z_balicku(1, stul)
    while color.black in stul[-1]:
        stul += vzit_z_balicku(1, stul)

    while True:
        for i in range(len(hraci)):
            global current_player
            index = (index + smer) % len(hraci)
            hrac = list(hraci.items())[index][0]

            global current_player
            current_player = hrac

            if len(balicek) == 0:
                balicek = vygeneruj_karty()
            print(f"Log hry:")
            print(*log[-5:], sep='')
            print(f"Na tahu je {color.bold}{hrac}{color.none}")
            tah(hraci[current_player])
            if len(hraci[current_player]) == 0:
                end_game()
            clear_screen()

def write_log(msg):
    global log
    log.append(f"{len(log) + 1}: {msg}")

def special_card_check(karta):
    # hrac pouzil STOP kartu
    if "∅" in karta:
        global stopped
        stopped = True

    if "⇔" in karta:
        global smer
        smer = -smer

    # zmena barvy
    if "BARVA" in karta:
        karta = zmenit_barvu("BARVA")
    elif "+4" in karta:
        karta = zmenit_barvu("+4")

    # dalsi bere +4/+2 pokud to neprebije
    if "+4" in karta or "+2" in karta:
        global plus_card_buffer
        plus_card_buffer.append(karta)
    return karta

def tah(karty):
    karta = vyber_kartu(karty)
    # hrac dobira
    if karta is None:
        write_log(
            f"{color.bold}{current_player}{color.none} dobral kartu. Počet karet na ruce: {color.bold}{len(players[current_player])}{color.none}\n")
        return

    # hrac zastaven STOP kartou
    if karta == "STOP":
        write_log(
            f"{color.bold}{current_player}{color.none} byl zastaven. Počet karet na ruce: {color.bold}{len(players[current_player])}{color.none}\n")
        input_hrac("Byl jste zastaven, jedno kolo nejedete ")
        return
    if "PC" in current_player: clear_screen()
    input_hrac(f"Zahráli jste {karta} ")

    karta = special_card_check(karta)

    dat_na_stul(karta, karty)
    write_log(
        f"{color.bold}{current_player}{color.none} zahrál {karta}. Počet karet na ruce: {color.bold}{len(players[current_player])}{color.none}\n")
    return karta

def get_symbol(karta):
    return karta[5:]

def get_color(karta):
    return karta[:5]

def end_game():
    clear_screen()
    print(f"{current_player} VYHRÁL!")
    input("Pokračujte stisknutím ENTER tlačítka do menu...")
    menu()

def dat_na_stul(karta, lst):
    if karta is None:
        return
    global table
    stul.append(karta)
    lst.remove(find_match(lst, karta, ["BARVA", "+4"]))

def find_match(lst, match, keywords):
    for item in lst:
        if item == match:
            return item
    for item in lst:
        if any(keyword in item for keyword in keywords):
            return item

def input_hrac(msg):
    if "PC" not in current_player:
        return input(msg)

def vyber_kartu(karty):
    volba = {0: 0}

    s = f"{color.bold}0)BRÁT{color.none} "
    for i in range(len(karty)):
        if hratelna_karta(karty[i]):
            volba.update({i + 1: karty[i]})
            s += f"{color.bold}{i + 1}){karty[i]}{color.none}  "
        else:
            s += f"{color.gray}{i + 1}){karty[i]}{color.none}  "

    print(f"""Stůl: {table[len(table) - 1]}
Karty: {s}""")

    if len(volba) == 1:  # není co hrát, ber karty
        if len(plus_card_buffer) != 0:  # dostal +4/+2
            bere_plus_karty(karty)
            return
        global stopped
        if stopped:
            stopped = False
            return "STOP"
        input_hrac("Nemůžete zahrát žádnou kartu, stiskněte tlačítko pro braní: ")
        input_hrac(f"Vybral jste {vzit_z_balicku(1, karty)[0]}")
        return

    if "PC" in current_player:
        vstup = list(volba)[-1]
    else:
        vstup = verfify_input("Zadejte číslo karty: ")
        while vstup not in volba.keys():
            vstup = verfify_input("Tuto kartu zahrát nemůžete. Zkuste to znovu: ")

    if vstup == 0:
        if len(plus_card_buffer) != 0:
            bere_plus_karty(karty)
            return
        input_hrac(f"Vybral jste {vzit_z_balicku(1, karty)[0]} ")
        return

    return karty[vstup - 1]

def bere_plus_karty(karty):
    global plus_card_buffer
    pocet = 0
    for i in plus_card_buffer:
        pocet += int(get_symbol(i)[1])
    plus_card_buffer = []
    input_hrac(f"Musíte brát {pocet} karet, stiskněte tlačítko pro braní: ")
    print("Vybral jste ", end="")
    print(*vzit_z_balicku(pocet, karty))
    input_hrac("")
    return

def verfify_input(msg):
    vstup = input_hrac(msg)
    while not vstup.isdecimal():
        vstup = input_hrac(msg)
    return int(vstup)

def hratelna_karta(karta):
    barva_karta = get_color(karta)
    symbol_karta = get_symbol(karta)
    barva_stul = get_color(table[len(table) - 1])
    symbol_stul = get_symbol(table[len(table) - 1])
    if barva_karta == barva_stul or symbol_karta == symbol_stul or barva_karta == color.black:
        if len(plus_card_buffer) > 0 and ("+4" not in karta and "+2" not in karta):
            return False
        if stopped and "∅" not in karta:
            return False
        return True
    return False

def zmenit_barvu(jmeno_karty):
    if "PC" in current_player:
        return f"{dominantni_barva(players[current_player])}{jmeno_karty}{color.none}"
    vstup = verfify_input(f"""Zadejte barvu, na kterou chcete změnit
{color.red}1 {color.blue}2 {color.green}3 {color.yellow}4{color.none}: """)
    volba = {1: color.red, 2: color.blue, 3: color.green, 4: color.yellow}
    while vstup not in volba.keys():
        vstup = verfify_input("Tato barva neexistuje. Zkuste to znovu: ")
    return f"{volba[vstup]}{jmeno_karty}{color.none}"

def dominantni_barva(karty):
    barvy = {color.red: 0, color.blue: 0, color.green: 0, color.yellow: 0}
    for karta in karty:
        try:
            barvy.update({get_color(karta): barvy[get_color(karta)] + 1})
        except:
            continue
    return [k for k, v in barvy.items() if v == max(barvy.values())][0]

def vzit_z_balicku(num, karty):
    global deck
    ls = balicek[:int(num)]
    balicek = balicek[num:]
    karty += ls
    return ls

def vygeneruj_karty():
    karty = []
    karty_normal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "∅", "⇔", "+2"]
    barvy = [color.red, color.blue, color.green, color.yellow]
    for i in range(len(barvy)):
        for j in range(len(karty_normal)):
            karty.append(f"{barvy[i]}{karty_normal[j]}{color.none}")
            if karty_normal[j] != 0:
                karty.append(f"{barvy[i]}{karty_normal[j]}{color.none}")
    for i in range(4):
        karty.append(f"{color.black}BARVA{color.none}")
        karty.append(f"{color.black}+4{color.none}")
    random.shuffle(karty)
    return karty

def pravidla():
    clear_screen()
    input("""--------
Pravidla:
https://cs.wikipedia.org/wiki/Uno_(karetn%C3%AD_hra)#Pravidla\n
Neplatí speciální schopnosti karet 0 a 7, není implementováno 'UNO' při poslední kartě (nemá smysl implementovat)

Stiskněte libovolnou klávesu pro návrat do menu.
---------""")
    menu()

menu()
