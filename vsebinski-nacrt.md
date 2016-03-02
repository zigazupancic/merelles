# Merelles (Mlin)
## Opis aplikacije
Ob zagonu aplikacije se odpre okno z igralno ploščo in igra se začne s privzetimi nastavitvami (ČLOVEK - ČLOVEK). Če želimo drugačne nastavitve, v meniju izberemo `Nova igra`. Človek premika poteze s klikom na žeton in nato na polje, kamor ga želi postaviti. 

Aplikacija je lahko v enem od treh stanj:
1. Nastavljanje nove igre
..* Izbira vrste igralcev
..* Težavnost igralca RAČUNALNIK, če je izbran
..* Imena igralcev
2. Igranje
..* Na plošči so vidni aktivni žetoni ter informacije o igri (kdo je na potezi in kaj mora narediti)
3. Konec igre
..* Izpiše se ime zmagovalca

## Struktura programa
Aplikacija je ločena na dva dela - logiko igre v datoteki `game-logic.py` in grafični vmesnik v datoteki `gui.py`.
### Razredi logike igre
#### Razred `Igra`
Objekt hrani podatke o trenutni postavitvi na igralnem polju, podatke o vseh žetonih, trenutnem igralcu in fazi igre.
Metode:
* `veljavna_poteza(self, zeton, zeljeno_polje)`: preveri, če dani žeton lahko postavimo na želeno polje glede na fazo igre
* `veljavne_poteze(self)`: vrne seznam vseh možnih potez igralca na potezi
* `stanje_igre(self)`: preveri v katerem stanju je igra - v kateri fazi (postavljanje žetonov, premikanje žetonov) ali konec igre
* `odigraj_potezo(self, zeton, polje)`: ustrezno posodobi podatke o žetonih in igralni plošči, sicer pokliče `zakljucek_poteze`
* `zakljucek_poteze(self, zeton)`: če je potrebno vzeti žeton ustrezno posodbi podatke o žetonih in igralni plošči ter pokliče metodo `stanje_igre`

#### Razreda `Clovek` in `Racunalnik`
Metode:
* `igraj(self)`: GUI pokliče metodo, ko je igralec na potezi
* `klik(self, koordinata, objekt)`: ko igralec klikne na ploščo, objekt je žeton ali polje na plošči
Atributi:
* `faza_poteze`: pove v kateri fazi poteze je igralec (izberi žeton za premik, izberi polje, izberi nasprotnikov žeton)

# Grafični vmesnik
* Ob zagonu igre se pojavi izbirno okno, kjer izberemo vrsto igralca, imena ter težavnost
* Ozadje: slika igralne plošče s prostorom za žetone pri strani, nad žetoni ime in vrsta igralca
* Vsak žeton ima svoje koordinate
* Vsako križišče ima navidezen krog, v katerem se žeton "prilepi" na križišče, če je v njem izpuščen
* Križišča so predstavljena s številko 0-23
* Žetoni se premikajo z vlečenjem miške
* Možne trojke so predstavljene s seznamom
* Sosedi vsakega križišča so zapisani v seznamu
* Pri preverjanju legalne poteze se preveri seznam sosedov križišča in prosta polja


