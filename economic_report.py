# PD1 Maja Żabińska
# Raport ekonomiczny sklepiku uczelnianego

def popraw_nazwe(nazwa: str) -> str:
    # typowanie funkcji + funkcje przetwarzajace lancuch znakow
    nazwa = nazwa.strip()
    nazwa = nazwa.replace("_", " ")
    return nazwa.title()


def opis_ryzyka(marza: float) -> str:
    # instrukcja match
    match marza:
        case marza if marza < 0:
            return "strata"
        case marza if marza < 0.10:
            return "niska marza"
        case marza if marza < 0.25:
            return "srednia marza"
        case _:
            return "wysoka marza"


def suma_przychodow(*kwoty: float) -> float:
    # zmienna liczba argumentow:*kwoty
    suma = 0
    for kwota in kwoty:
        suma += kwota
    return suma


def oblicz_cene_brutto(cena_netto: float, podatek: float = 0.23) -> float:
    # argument domyslny funkcji: podatek 23%
    def dolicz_podatek(cena: float) -> float:
        # funkcja zagniezdzona
        return cena * (1 + podatek)

    return dolicz_podatek(cena_netto)


def przygotuj_raport(nazwa_firmy: str, produkty: list, waluta: str = "PLN") -> str:
    # argument domyslny funkcji:waluta="PLN"
    raport = "RAPORT EKONOMICZNY\n"
    raport += f"Firma: {popraw_nazwe(nazwa_firmy)}\n"  # formatowanie lancucha znakow: f-string
    raport += "-" * 50 + "\n"

    rabat: float = 0.05  # typowanie zmiennej
    kategorie_marzy = (opis_ryzyka(produkt["marza"]) for produkt in produkty)
    # generator: wyrazenie generatorowe

    pierwszy_produkt = iter(produkty)
    # iterator 
    produkt_startowy = next(pierwszy_produkt)
    raport += f"Pierwszy analizowany produkt: {produkt_startowy['nazwa']}\n\n"

    przychody = []

    for produkt in produkty:
        nazwa = popraw_nazwe(produkt["nazwa"])
        cena_brutto = oblicz_cene_brutto(produkt["cena"], podatek=0.23)
        # argument nazwany funkcji: podatek 23%

        cena_po_rabacie = cena_brutto * (1 - rabat) if produkt["sprzedaz"] > 50 else cena_brutto
        # operator warunkowy 

        przychod = cena_po_rabacie * produkt["sprzedaz"]
        przychody.append(przychod)

        kategoria = next(kategorie_marzy)

        if "usluga" in produkt["typ"]:
            # operator przynaleznosci: in
            rodzaj = "produkt uslugowy"
        else:
            rodzaj = "produkt materialny"

        raport += "Produkt: {}\n".format(nazwa)  # formatowanie lancucha znakow
        raport += f"Typ: {rodzaj}\n"
        raport += f"Cena brutto: {cena_brutto:.2f} {waluta}\n"
        raport += f"Cena po rabacie: {cena_po_rabacie:.2f} {waluta}\n"
        raport += f"Sprzedaz: {produkt['sprzedaz']} szt.\n"
        raport += f"Przychod: {przychod:.2f} {waluta}\n"
        raport += f"Ocena marzy: {kategoria}\n"
        raport += "-" * 50 + "\n"

    laczny_przychod = suma_przychodow(*przychody)
    raport += f"Laczny przychod: {laczny_przychod:.2f} {waluta}\n"

    return raport


def zapisz_raport(tresc: str, nazwa_pliku: str = "raport_ekonomiczny.txt") -> None:
    # instrukcja with
    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        plik.write(tresc)


produkty: list = [
    {"nazwa": "  kawa_rozpuszczalna  ", "typ": "towar", "cena": 12.50, "sprzedaz": 80, "marza": 0.30},
    {"nazwa": "kurs_excela", "typ": "usluga edukacyjna", "cena": 180.00, "sprzedaz": 18, "marza": 0.22},
    {"nazwa": "notatnik_finansowy", "typ": "towar", "cena": 25.00, "sprzedaz": 45, "marza": 0.08},
    {"nazwa": "konsultacja_biznesowa", "typ": "usluga doradcza", "cena": 250.00, "sprzedaz": 8, "marza": -0.02},
]

raport_koncowy = przygotuj_raport("  sklep_SGH  ", produkty, waluta="PLN")
# argument nazwany funkcji: waluta="PLN"

print(raport_koncowy)

zapisz_raport(raport_koncowy)
