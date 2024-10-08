import mysql.connector
from geopy import distance
#Kommenteissa lukee vielä mitä pitäisi lisätä

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='demogame',
    user='root',
    password='salasana',
    autocommit=True
)


player_data = {
    'name': "",
    'raha': 500,
    'xp': 0,
    'omistetut_koneet': 1,
    'suoritetut_keikat': 0,
    'omistettu_bensa': 0,
    'nykyinen_kone': None
}
Lentokone =[
       {
     'nimi': 'Pienenmatkan Lentokone',
        'maksimi_bensa': 4,
        'nykyinen_bensa': 4,
        'hinta': 500
    },
{
        'nimi': 'Keskipitkänmatkan Lentokone',
        'maksimi_bensa': 6,
        'nykyinen_bensa': 6,
        'hinta': 1000
    },
{
        'nimi': 'Pitkänmatkan Lentokone',
        'maksimi_bensa': 10,
        'nykyinen_bensa': 10,
        'hinta': 1500
    },

]

def paivitus():
    try:
        kursori = yhteys.cursor()
        sql = """
        UPDATE pelaaja 
        SET raha = %s, kokemus = %s, omistetut_koneet = %s, tehdyt_keikat = %s, bensa = %s 
        WHERE id = 1
        """
        data = (player_data['raha'], player_data['xp'], player_data['omistetut_koneet'],
                player_data['suoritetut_keikat'], player_data['omistettu_bensa'])
        kursori.execute(sql, data)
        yhteys.commit()
    finally:
        kursori.close()

def alustitaan_taulu():
    try:
        sql = "INSERT INTO pelaaja (id, nimi, raha, kokemus, omistetut_koneet, tehdyt_keikat, bensa) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (1, player_data['name'], player_data['raha'], player_data['xp'],
        player_data['suoritetut_keikat'], player_data['omistetut_koneet'],
        player_data['omistettu_bensa'])

        mycursor = yhteys.cursor()
        mycursor.execute(sql, val)
        yhteys.commit()
    finally:
        mycursor.close()

def lataa_peli(pelaajan_nimi):
    kursori = yhteys.cursor()
    sql = "SELECT nimi, omistetut_koneet, raha, kokemus, tehdyt_keikat, bensa FROM pelaaja WHERE nimi = %s"
    kursori.execute(sql, (pelaajan_nimi,))
    result = kursori.fetchone()
    if result:
        player_data.update({
            'name': result[0],
            'raha': result[2],
            'xp': result[3],
            'omistetut_koneet': result[1],
            'suoritetut_keikat': result[4],
            'omistettu_bensa': result[5]
        })
        return True
    return False

def hae_lentokentta_ja_koordinaatisto(lentokentta_ident):
    kursori = yhteys.cursor()
    sql = f"SELECT longitude_deg, latitude_deg FROM airport WHERE ident LIKE '{lentokentta_ident}'"
    kursori.execute(sql)
    koordinaatit = kursori.fetchall()
    return koordinaatit[0]


viron_koordinaatit = hae_lentokentta_ja_koordinaatisto('EETN')
turun_koordinaatit = hae_lentokentta_ja_koordinaatisto('EFTU')
latvian_koordinaatit = hae_lentokentta_ja_koordinaatisto('EVRA')
saksan_koordinaatit = hae_lentokentta_ja_koordinaatisto('EDDB')
britannia_koordinaatit = hae_lentokentta_ja_koordinaatisto('EGLL')
espanja_koordinaatit = hae_lentokentta_ja_koordinaatisto('LEMD')
amerikka_koordinaatit = hae_lentokentta_ja_koordinaatisto('KJFK')
japani_koordinaatit = hae_lentokentta_ja_koordinaatisto('RJAA')


def aloita_peli():
    while True:
        print("***CARGO SIMULATOR***")
        print("[1] Uusi peli")
        print("[2] Lataa peli")
        print("[3] Sulje sovellus")
        valinta = input("Valitse 1, 2 tai 3: ")

        if valinta == "1":
            pelaajan_nimi = input("Anna nimi: ")
            player_data['name'] = pelaajan_nimi
            alustitaan_taulu()
            peli_tarina()
        elif valinta == "2":
            pelaajan_nimi = input("Anna ladattavan pelin nimi: ")
            if lataa_peli(pelaajan_nimi):
                print(f"Peli ladattu onnistuneesti pelaajalle {pelaajan_nimi}!")
                peli_tarina()
            else:
                print("Pelaajaa ei löytynyt, yritä uudelleen.")
        elif valinta == "3":
            print("Suljetaan sovellus...")
            break
        else:
            print("Valitse 1, 2 tai 3.")

def peli_tarina():
    print("Heräät... et ole varma mistä...?")
    print("Paikka näyttää täysin tuntemaltasi Suomen maalta, mutta kaikista on muuttunut alieneita.")
    print("...")
    print("Toivot, että tämä olisi vain pahaa unta...")
    print("...")
    print("Mutta sitten näet KELAN!! Voisiko tämä olla ratkaisu kaikkeen?!?!")
    print("Kela lahjoittaa sinulle rikkinäisen aloitus lentokoneen, jolla voit aloittaa rahdin kuljetus firman.")
    print("Mitään muutakaan et voi, joten päätät ryhtyä tämän planeetan parhaaksi cargon välittäjäksi!")
    print("Jotta jonain päivänä, voit palata omalle koti-planeetallesi, koti SUOMEEEN...")
    print("...")
    pelin_paa_valikko()

def hae_aloitus_koorinaatit():
    kursori = yhteys.cursor()
    sql = f"SELECT longitude_deg, latitude_deg FROM airport WHERE ident LIKE 'EFHK'"
    kursori.execute(sql)
    suomi_koord = kursori.fetchall()
    return suomi_koord


aloitus_koordinaatit = hae_aloitus_koorinaatit()


def laske_vali(aloitus_koordinaatit):
#GEOPY=round(distance((coord1[1], coord1[0]), (coord2[1], coord2[0])).km, 2)
    suomi_viro_vali = round(distance.distance(aloitus_koordinaatit[0], viron_koordinaatit[0]).km, 2)
    suomi_turku_vali = round(distance.distance(aloitus_koordinaatit[0], turun_koordinaatit[0]).km, 2)
    suomi_latvia_vali = round(distance.distance(aloitus_koordinaatit[0], latvian_koordinaatit[0]).km, 2)
    suomi_saksa_vali = round(distance.distance(aloitus_koordinaatit[0], saksan_koordinaatit[0]).km, 2)
    suomi_japani_vali = round(distance.distance(aloitus_koordinaatit[0], japani_koordinaatit[0]).km, 2)
    suomi_britannia_vali = round(distance.distance(aloitus_koordinaatit[0], britannia_koordinaatit[0]).km, 2)
    suomi_espanja_vali = round(distance.distance(aloitus_koordinaatit[0], espanja_koordinaatit[0]).km, 2)
    suomi_amerikka_vali = round(distance.distance(aloitus_koordinaatit[0], amerikka_koordinaatit[0]).km, 2)
    return suomi_viro_vali, suomi_turku_vali, suomi_latvia_vali, suomi_saksa_vali, suomi_japani_vali, suomi_britannia_vali, suomi_espanja_vali, suomi_amerikka_vali

def pelin_paa_valikko():
    while True:
        print("\n[1] Keikat")
        print("[2] Kauppa")
        print("[3] Status")
        print("[4] Sulje sovellus")
        valinta = input("Valitse 1, 2, 3 tai 4: ")
        if valinta == "1":
            keikat()
        elif valinta == "2":
            kauppa()
        elif valinta == "3":
            status()
        elif valinta == "4":
            print("Suljetaan sovellus...")
            yhteys.close()
            exit()
        else:
            print("Valitse validi vaihtoehto.")

# kauppa josta pelaaja voi ostaa koneita sekä bensaa
def kauppa():
    while True:
        print("\n*** Tervetuloa Kauppaan! ***")
        print("------------------------------")
        print("[1] Osta Bensakanisteri (50€)")
        print("[2] Osta Pienenmatkan Lentokone (500 €)")
        print("[3] Osta Keskipitkänmatkan Lentokone (1000 €)")
        print("[4] Osta Pitkänmatkan Lentokone (1500 €)")
        print("[6] Osta Raketti (Voitit Pelin) (5000 €)")
        print("[0] Takaisin päävalikkoon")

        valinta = input("Valitse osto (numero) tai 0: ")

        if valinta == "0":
            pelin_paa_valikko()

        elif valinta == "1":
            # Näytetään vain omistetut koneet
            if player_data['omistetut_koneet'] > 0:
                print("\nValitse lentokone johon bensaa lisätään:")
                # Suodatetaan vain omistetut koneet
                omistetut_koneet = Lentokone[:player_data['omistetut_koneet']]
                for idx, kone in enumerate(omistetut_koneet):
                    print(
                        f"[{idx + 1}] {kone['nimi']} - Nykyinen bensa: {kone['nykyinen_bensa']}/{kone['maksimi_bensa']}")

                kone_valinta = int(input("Valitse lentokone (numero): ")) - 1
                valittu_kone = omistetut_koneet[kone_valinta]

                # Tarkistetaan raha ja lisätään bensa
                if player_data['raha'] >= 50:
                    if valittu_kone['nykyinen_bensa'] < valittu_kone['maksimi_bensa']:
                        player_data['raha'] -= 50
                        valittu_kone['nykyinen_bensa'] += 1
                        if valittu_kone['nykyinen_bensa'] > valittu_kone['maksimi_bensa']:
                            valittu_kone['nykyinen_bensa'] = valittu_kone['maksimi_bensa']
                        print(
                            f"Ostit 1 bensakanisterin! {valittu_kone['nimi']} nykyinen bensa: {valittu_kone['nykyinen_bensa']}/{valittu_kone['maksimi_bensa']}.")
                    else:
                        print(
                            f"{valittu_kone['nimi']} bensa on jo täysi ({valittu_kone['maksimi_bensa']}/{valittu_kone['maksimi_bensa']}).")
                else:
                    print("Sinulla ei ole tarpeeksi rahaa ostaaksesi bensakanisteria.")
            else:
                print("Sinulla ei ole yhtään omistettua lentokonetta.")

        elif valinta == "2":
            if player_data['raha'] >= 500:
                player_data['raha'] -= 500
                player_data['omistetut_koneet'] += 1
                Lentokone[0]['nykyinen_bensa'] = Lentokone[0]['maksimi_bensa']
                print(
                    f"Ostit {Lentokone[0]['nimi']}! Nykyinen bensa: {Lentokone[0]['nykyinen_bensa']}/{Lentokone[0]['maksimi_bensa']}.")
            else:
                print("Sinulla ei ole tarpeeksi rahaa ostaaksesi lentokonetta.")

        elif valinta == "3":
            if player_data['raha'] >= 1000:
                player_data['raha'] -= 1000
                player_data['omistetut_koneet'] += 1
                Lentokone[1]['nykyinen_bensa'] = Lentokone[1]['maksimi_bensa']
                print(
                    f"Ostit {Lentokone[1]['nimi']}! Nykyinen bensa: {Lentokone[1]['nykyinen_bensa']}/{Lentokone[1]['maksimi_bensa']}.")
            else:
                print("Sinulla ei ole tarpeeksi rahaa ostaaksesi lentokonetta.")

        elif valinta == "4":
            if player_data['raha'] >= 1500:
                player_data['raha'] -= 1500
                player_data['omistetut_koneet'] += 1
                Lentokone[2]['nykyinen_bensa'] = Lentokone[2]['maksimi_bensa']
                print(
                    f"Ostit {Lentokone[2]['nimi']}! Nykyinen bensa: {Lentokone[2]['nykyinen_bensa']}/{Lentokone[2]['maksimi_bensa']}.")
            else:
                print("Sinulla ei ole tarpeeksi rahaa ostaaksesi lentokonetta.")

        elif valinta == "6":
            if player_data['raha'] >= 5000:
                player_data['raha'] -= 5000
                player_data['omistetut_koneet'] += 1
                print("Ostit Raketin!")
                print("Lähdit avaruuteen etsimään kotiplaneettaasi!")
                yhteys.close()
                exit()
            else:
                print("Sinulla ei ole tarpeeksi rahaa ostaaksesi rakettia.")

        else:
            print("Valitse numero 1, 2, 3, 4, 6 TAI 0")

# keikat pelaajalle
def keikat():
    global player_data

    # jos pelaajalla ei ole konetta
    if player_data['omistetut_koneet'] == 0:
        print("\nEt omista yhtään lentokonetta. Käy ensin ostamassa lentokone kaupasta.")
        return

    # pelaaja valitsee omistaman koneen
    if player_data['omistetut_koneet'] > 1:
        print("\nValitse lentokone keikkaa varten:")
        for idx, kone in enumerate(Lentokone):
            if player_data['omistetut_koneet'] > idx:  # Tarkistetaan, omistaako pelaaja kyseisen koneen
                print(f"[{idx + 1}] {kone['nimi']} - Nykyinen bensa: {kone['nykyinen_bensa']}/{kone['maksimi_bensa']}")
        kone_valinta = int(input("Valitse lentokone (numero): ")) - 1

        if kone_valinta >= player_data['omistetut_koneet']:
            print("Et omista valitsemaasi lentokonetta.")
            return

        player_data['nykyinen_kone'] = kone_valinta
        valittu_kone = Lentokone[kone_valinta]
    else:
        valittu_kone = Lentokone[0]
        player_data['nykyinen_kone'] = 0

    # määritellään keikat
    missions = [
        ("Viron keikka", 1, 200, 150, 2),
        ("Turun keikka", 1, 150, 100, 1),
    ]
    mission1 = [
        ("Latvian keikka", 1, 400, 200, 3),
        ("Saksan keikka", 1, 550, 700, 4),
        ("Britannian keikka", 1, 700, 400, 4),
    ]
    mission2 = [
        ("Espanjan keikka", 1, 750, 750, 4),
        ("Japanin keikka", 1, 600, 1000, 5),
        ("Amerikan keikka", 1, 1000, 100, 6),
    ]

    # pelaajan keikat
    while True:
        print("\n*** Valitse Keikka ***")

        print("\n-- Alkutason keikat (0-500 XP) --")
        for index, mission in enumerate(missions):
            if player_data['xp'] >= 0:
                print(f"[{index + 1}] {mission[0]} (Palkka: {mission[2]}€, Kokemuspisteet: {mission[3]} XP, Bensankulutus: {mission[4]} kanisteria)")

        if player_data['xp'] >= 500:
            print("\n-- Keskitaso (500+ XP) --")
            for index, mission in enumerate(mission1):
                print(f"[{index + 1 + len(missions)}] {mission[0]} (Palkka: {mission[2]}€, Kokemuspisteet: {mission[3]} XP, Bensankulutus: {mission[4]} kanisteria)")

        if player_data['xp'] >= 2000:
            print("\n-- Edistynyt taso (2000+ XP) --")
            for index, mission in enumerate(mission2):
                print(f"[{index + 1 + len(missions) + len(mission1)}] {mission[0]} (Palkka: {mission[2]}€, Kokemuspisteet: {mission[3]} XP, Bensankulutus: {mission[4]} kanisteria)")

        print("[0] Takaisin päävalikkoon")
        valinta = input("Valitse keikka (numero) tai 0: ")

        if valinta == "0":
            pelin_paa_valikko()
            return

        try:
            index = int(valinta) - 1

            if index < len(missions):
                keikka_nimi, distance, palkka, xp, bensa = missions[index]
            elif index < len(missions) + len(mission1) and player_data['xp'] >= 500:
                keikka_nimi, distance, palkka, xp, bensa = mission1[index - len(missions)]
            elif index < len(missions) + len(mission1) + len(mission2) and player_data['xp'] >= 2000:
                keikka_nimi, distance, palkka, xp, bensa = mission2[index - len(missions) - len(mission1)]
            else:
                print("Virheellinen valinta tai kokemuspisteet eivät riitä keikkaan!")
                continue
                # tarkistetaan onko bensaa
            if valittu_kone['nykyinen_bensa'] >= bensa:
                valittu_kone['nykyinen_bensa'] -= bensa
                player_data['raha'] += palkka
                player_data['xp'] += xp
                player_data['suoritetut_keikat'] += 1
                print(f"Keikka '{keikka_nimi}' suoritettu!")
                print(f"Ansaitsit {palkka}€, ja saat {xp} XP!")
                print(f"Sinulla on nyt {player_data['raha']}€ ja {valittu_kone['nykyinen_bensa']}/{valittu_kone['maksimi_bensa']} kanisteria bensiiniä jäljellä.")
                paivitus()
            else:
                print(f"Sinulla ei ole tarpeeksi bensaa {valittu_kone['nimi']} keikkaan!")

        except ValueError:
            print("Onko näössä ongelmia.")

# näytetään pelaajalle tiedot
def status():
    print("***Pelaajan Status***")
    print(f"Nimi: {player_data['name']}")
    print(f"Rahat: {player_data['raha']}€")
    print(f"Kokemuspisteet: {player_data['xp']} XP")
    print(f"Omistettuja koneita: {player_data['omistetut_koneet']}")
    print(f"Tehtyjä keikkoja: {player_data['suoritetut_keikat']}")
    if player_data['nykyinen_kone'] is not None:
        kone = Lentokone[player_data['nykyinen_kone']]
        print(f"Nykyinen kone: {kone['nimi']}")
        print(f"Bensaa jäljellä: {kone['nykyinen_bensa']}/{kone['maksimi_bensa']}")
    else:
        print("Sinulla on vain rikkinäinen lahjoitettu lentokone...")


aloita_peli()