# Domnělá inteligence nepíše nic inteligentního, jen to tak vypadá. Použije poslední 2 slova ze vstupu a vybere náhodné slovo,
# které navazuje na ta 2 předchozí v nějakém ze zdrojových textů (články z Wikipedie na témata: klopný obvod, komplexní čísla, útoky 11. září, holokaust, Václav III., Martin Luther King, NDR, Velká Morava,
# rybník Podlesník, Engelova klasifikace, speciální čarodějnický díl 33 Simpsnovi, vesnice Doubrava, cyklistický závod Paříž-Roubaix, román Cesta nikam, hora Veliki Planik, zlatý míč, Blizzard Entertainment,
# železniční stanice Valšov, kanton Grenoble-1, počítač Zotac VR GO, Windows 10, elektronvolt, Esperanto, meteoroid EN131090, Právnická fakulta Masarykovy univerzity, druhá křížová výprava, Škoda Felicia,
# Přemysl Otakar II., vznik a vývoj sluneční soustavy, Zbraslavský klášter, DNA, jedle, růže, bowling, holubí fotografie ze vzduchu, Městské divadlo Brno, Niizuki, Šalomounovy ostrovy, Saturn I, Oběžná dráha,
# Staroměstský orloj, Sluneční čas, Měsíční fáze, Varnsdorf, Obec s rozšířenou působností, Václav II., Vražda Johna Lennona, Hazardní hra).
# Aby nemusel program neustále prohledávat zdrojový text, nejdřív vytvoří set unikátních slov*, každému přiřadí index, a vytvoří 2 slovníky na kódování a dekódování.
# Postupně pak bere každé téma ze zdrojového textu, a přidá do listu na indexu 1. slova do slovníku na indexu 2. slova 3. slovo. Tím vznikne seznam všech možných slov pro každou dvojici předcházejících,
# ze kterého je pak náhodně vybráno slovo, které Domnělá inteligence napíše. Pak se druhé slovo přesune na první a třetí na druhé a pokračuje se dál dokud nebude mít text 10 vět (teček) nebo 1000 Domnělých tokenů,
# podle toho, co nastane dříve. V případě neexistuícího slova porovná podobnost (součet počtu nutných náhrad, ostranění a přidání znaků) tohoto slova s listem všech slov (který začíná v náhodném místě,
# takže se slovo nemusí vždy opravit na stejné, to proto, aby byla Domnělá inteligence ještě méně spolehlivá), a toto slovo použije.
# *Domnělá inteligence využívá Domnělé tokeny, tedy nerozděluje jen na mezerách, ale odděluje od slov i tyto znaky: .,?:+-*/()[]<>



import time, random
from data import texty

t = time.time()
pocetDT = data = 0
indexy = {}
revindexy = {}
slova = []

def split(s):
    ret = [""]
    for i in s:
        if i == " ": ret.append("")
        elif i in ".,?:+-*/()[]<>": ret.append(i)
        else: ret[-1] += i
    return ret

for index, slovo in enumerate(set(slovo for text in texty for slovo in split(text))):
    indexy[slovo] = index
    revindexy[index] = slovo
    slova.append({})

for text in texty:
    data += text.__sizeof__()
    text = [indexy[slovo] for slovo in split(text)]
    text += text[:2]
    pocetDT += len(text) - 2
    for i in range(2, len(text)):
        if text[i-1] in slova[text[i-2]].keys():
            slova[text[i-2]][text[i-1]].append(text[i])
        else:
            slova[text[i-2]][text[i-1]] = [text[i]]

print(f"Domnělá inteligence®\nData: {data/1048576:.2f} MB\nRychlost trénování: {(time.time()-t)/data*1048576000:.2f} ms/MB\nPočet Domnělých tokenů: {pocetDT/1000:.1f} tisíc ({len(indexy)/1000:.1f} tisíc unikátních)\n\n\nVýstupy generované Domnělou inteligencí® mohou obsahovat informace, které jsou přesné a správné. V některých situacích tak mohou být tyto informace velmi užitečné, například při matematických výpočtech, faktografických údajích nebo základních definicích z různých oblastí. Uživatel nese veškerou odpovědnost za případné pozitivní výsledky, které mohou vzniknout v důsledku využití odpovědí Domnělé inteligence®.\n")

def podobnost(slovo1, slovo2):
    m = [list(range(len(slovo2) + 1))] + [[i+1] + [0 for _ in range(len(slovo2))] for i in range(len(slovo1))]
    for i in range(len(slovo1)):
        for j in range(len(slovo2)):
            a = m[i][j]+int(slovo1[i] != slovo2[j])-1
            b = m[i][j+1]
            c = m[i+1][j]
            m[i+1][j+1] = ((b if b < c else c) if a > c else a) if a < b else (c if b > c else b)
    return -m[-1][-1]

def nejpodobnejsi(slovo):
    slovnik = list(indexy.keys())
    if slovo in slovnik: return slovo
    nej = ""
    nej2 = float("-infinity")
    r = random.randint(0, len(indexy))
    slovnik = slovnik[r:] + slovnik[:r]
    for s in slovnik:
        p = podobnost(slovo, s)
        if p > nej2:
            nej2 = p
            nej = s
    return nej

while not False:
    s = input(">>> ")
    s = s if s else "Klopný obvod je"
    s1, s2 = tuple(i for i in split(s)[-2:])
    s1 = nejpodobnejsi(s1)
    s2 = nejpodobnejsi(s2)
    print(s1, s2, end="")
    s1 = indexy[s1]
    s2 = indexy[s2]
    vety, i = 0, 0
    while vety < 10 and i < 1000:
        s3 = random.choice(slova[s1][s2])
        print((" " if revindexy[s3] not in ".,?:+-*/()[]<>" else "") + revindexy[s3], end="")
        vety += int(revindexy[s3] == ".")
        s1, s2 = s2, s3
        i += 1
    print()
