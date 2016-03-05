# Merelles (Mlin)
## Opis aplikacije
Ob zagonu aplikacije se odpre okno z igralno ploščo in igra se začne s privzetimi nastavitvami (ČLOVEK - ČLOVEK). Če želimo drugačne nastavitve, v meniju izberemo `Nova igra`. Človek premika poteze s klikom na žeton in nato na polje, kamor ga želi postaviti. 

Aplikacija je lahko v enem od treh stanj:

1. Nastavljanje nove igre
  * Izbira vrste igralcev
  * Težavnost igralca RAČUNALNIK, če je izbran
  * Imena igralcev
2. Igranje
  * Na plošči so vidni aktivni žetoni ter informacije o igri (kdo je na potezi in kaj mora narediti)
3. Konec igre
  * Izpiše se ime zmagovalca

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

### Razredi grafičnega vmesnika
#### Razred `GUI`
Objekt ustvari igralno ploščo ter prične novo igro s privzetimi nastavitvami (pokliče se metoda `nova_igra`).
Metode:
* `nova_igra(self, igralec_1, igralec_2, tezavnost=3)`: ponastavi žetone na igralni plošči, ustvari objekta razredov `igralec_1` in `igralec_2` ter objekt razreda `Igra`
* `koncaj_igro(self, zmagovalec=None)`: konča igro in izpiše zamgovalca
* `prestavi_zeton(self, zeton, polje)`: prestavi žeton na izbrano polje
* `odstrani_zeton(self, zeton)`: odstrani žeton iz igralnega polja
* `klik(self, event)`: objektu igralca, ki je na potezi povemo, da je uporabnik kliknil na ploščo in vrnemo (koordinata, objekt), kjer je objekt žeton ali polje (odvisno na kaj je kliknil)
* `povleci_potezo(self, vrsta_poteze, zeton, polje=None)`: premaknemo žeton na polje, oziroma vzamemo žeton, odvisno od vrste poteze

#### Razreda `Clovek` in `Racunalnik`
Metode:
* `igraj(self)`: GUI pokliče metodo, ko je igralec na potezi
* `klik(self, koordinata, objekt)`: ko igralec klikne na ploščo, objekt ustrezno ukrepa (spremeni fazo poteze ali pokliče `povleci_potezo`), objekt je žeton ali polje na plošči
Atributi:
* `faza_poteze`: pove v kateri fazi poteze je igralec (izberi žeton za premik, izberi polje, izberi nasprotnikov žeton)
