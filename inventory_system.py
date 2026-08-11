"""
Program obsługujący magazyn w przedsiębiorstwie handlowym

Funkcje programu:
 1. Tworzenie różnych typów produktów przechowywanych w magazynie
 2. Dodawanie produktów do magazynu
 3. Rejestrowanie dostaw (zwiększanie ilości produktu na stanie)
 4. Rejestrowanie wydań lub sprzedaży (zmniejszanie ilości produktu na stanie)
 5. Wyświetlanie raportu magazynowego wraz z opisem produktów i wartością magazynu
"""

from abc import ABC, abstractmethod


class Produkt(ABC):
    """Abstrakcyjna klasa bazowa dla produktów w magazynie."""

    def __init__(self, kod, nazwa, cena, ilosc):
        self.kod = kod
        self.nazwa = nazwa
        self._cena = 0
        self._ilosc = 0
        self.ustaw_cene(cena)
        self.dodaj_ilosc(ilosc)

    def pobierz_cene(self):
        return self._cena

    def pobierz_ilosc(self):
        return self._ilosc

    def ustaw_cene(self, cena):
        if cena > 0:
            self._cena = cena
        else:
            print("Cena musi być większa od zera.")

    def dodaj_ilosc(self, ilosc):
        if ilosc > 0:
            self._ilosc += ilosc
        else:
            print("Ilość dodawanego towaru musi być większa od zera.")

    def zdejmij_ilosc(self, ilosc):
        if ilosc <= 0:
            print("Ilość wydawanego towaru musi być większa od zera.")
            return False
        elif ilosc <= self._ilosc:
            self._ilosc -= ilosc
            return True
        else:
            print(f"Brak wystarczającej ilości produktu: {self.nazwa}")
            return False

    def wartosc(self):
        return self._cena * self._ilosc

    @abstractmethod
    def opis(self):
        pass


class ProduktSpozywczy(Produkt):
    """Klasa produktu spożywczego."""

    def __init__(self, kod, nazwa, cena, ilosc, termin_waznosci):
        super().__init__(kod, nazwa, cena, ilosc)
        self.termin_waznosci = termin_waznosci

    def opis(self):
        return (f"{self.kod} | {self.nazwa} | produkt spożywczy | "
                f"cena: {self._cena:.2f} zł | ilość: {self._ilosc} | "
                f"termin ważności: {self.termin_waznosci}")


class ProduktElektroniczny(Produkt):
    """Klasa produktu elektronicznego."""

    def __init__(self, kod, nazwa, cena, ilosc, miesiace_gwarancji):
        super().__init__(kod, nazwa, cena, ilosc)
        self.miesiace_gwarancji = miesiace_gwarancji

    def opis(self):
        return (f"{self.kod} | {self.nazwa} | produkt elektroniczny | "
                f"cena: {self._cena:.2f} zł | ilość: {self._ilosc} | "
                f"gwarancja: {self.miesiace_gwarancji} mies.")


class ProduktBiurowy(Produkt):
    """Klasa produktu biurowego."""

    def __init__(self, kod, nazwa, cena, ilosc, jednostka):
        super().__init__(kod, nazwa, cena, ilosc)
        self.jednostka = jednostka

    def opis(self):
        return (f"{self.kod} | {self.nazwa} | produkt biurowy | "
                f"cena: {self._cena:.2f} zł | ilość: {self._ilosc} {self.jednostka}")


class Magazyn:
    """Klasa reprezentująca magazyn przedsiębiorstwa."""

    def __init__(self, nazwa):
        self.nazwa = nazwa
        self._produkty = []

    def dodaj_produkt(self, produkt):
        self._produkty.append(produkt)

    def znajdz_produkt(self, kod):
        for produkt in self._produkty:
            if produkt.kod == kod:
                return produkt
        return None

    def przyjmij_dostawe(self, kod, ilosc):
        produkt = self.znajdz_produkt(kod)
        if produkt is not None:
            produkt.dodaj_ilosc(ilosc)
            print(f"Przyjęto dostawę: {produkt.nazwa}, ilość: {ilosc}")
        else:
            print(f"Nie znaleziono produktu o kodzie: {kod}")

    def wydaj_towar(self, kod, ilosc):
        produkt = self.znajdz_produkt(kod)
        if produkt is not None:
            if produkt.zdejmij_ilosc(ilosc):
                print(f"Wydano z magazynu: {produkt.nazwa}, ilość: {ilosc}")
        else:
            print(f"Nie znaleziono produktu o kodzie: {kod}")

    def wartosc_magazynu(self):
        suma = 0
        for produkt in self._produkty:
            suma += produkt.wartosc()
        return suma

    def raport(self):
        print("\nRAPORT MAGAZYNU")
        print(f"Magazyn: {self.nazwa}")
        print("-" * 90)

        for produkt in self._produkty:
            # Polimorfizm - dla każdego obiektu wywoływana jest jego własna metoda opis().
            print(produkt.opis())

        print("-" * 90)
        print(f"Łączna wartość magazynu: {self.wartosc_magazynu():.2f} zł")


def uruchom_program():
    magazyn = Magazyn("Magazyn główny firmy To i owo")

    smietana = ProduktSpozywczy("S001", "Smietana 30%", 3.99, 100, "2026-08-31")
    telefon = ProduktElektroniczny("E001", "Telefon Smart X", 1500.00, 8, 24)
    papier = ProduktBiurowy("B001", "Papier A4", 18.30, 40, "ryz")

    magazyn.dodaj_produkt(smietana)
    magazyn.dodaj_produkt(telefon)
    magazyn.dodaj_produkt(papier)

    magazyn.raport()

    print("\nOPERACJE MAGAZYNOWE")
    magazyn.przyjmij_dostawe("S001", 30)
    magazyn.wydaj_towar("E001", 2)
    magazyn.wydaj_towar("B001", 10)
    magazyn.wydaj_towar("E001", 20)

    magazyn.raport()


uruchom_program()
