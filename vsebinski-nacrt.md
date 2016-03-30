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
Aplikacija je ločena na dva dela - logiko igre v datoteki `game_logic.py` in grafični vmesnik z igralci v datoteki `gui.py`.
### Razredi logike igre
#### Razred `Igra`
Objekt hrani podatke o trenutni postavitvi na igralnem polju, podatke o vseh žetonih, trenutnem igralcu, zgodovini in fazi igre.
Metode:
* `veljavna_poteza(self, zeton, zeljeno_polje)`: preveri, če dani žeton lahko postavimo na želeno polje glede na fazo igre
* `veljavne_poteze(self)`: vrne seznam vseh možnih potez igralca na potezi
* `veljavni_zakljucek(self, zeton)`: preveri, če je veljavno vzeti `zeton`
* `veljavni_zakljucki(self)`: vrne seznam vseh veljavnih zaključkov
* `stanje_igre(self)`: preveri v katerem stanju je igra - v kateri fazi (postavljanje žetonov, premikanje žetonov) ali konec igre
* `odigraj_potezo(self, zeton, polje)`: ustrezno posodobi podatke o žetonih in igralni plošči, sicer pokliče `zakljucek_poteze`
* `zakljucek_poteze(self, zeton)`: če je potrebno vzeti žeton ustrezno posodbi podatke o žetonih in igralni plošči ter pokliče metodo `stanje_igre`
* `ocena_postavitve(self)`: oceni trenutno postavitev igralne plošče za prvega igralca
* `shrani_zgodovino(self)`: shrani trenutne podatke o plošči in ostalih atributih

### Razredi grafičnega vmesnika
#### Razred `GUI`
Objekt ustvari igralno ploščo ter prične novo igro s privzetimi nastavitvami (pokliče se metoda `nova_igra`).
Metode:
* metode `o_igri(self)`, `pomoc(self)`, `izbira_nove_igre(self)` ustvarijo ustrezna okna
* `nova_igra(self, igralec_1, igralec_2, tezavnost=2)`: ponastavi žetone na igralni plošči, ustvari objekta razredov `igralec_1` in `igralec_2` ter objekt razreda `Igra`
* `koncaj_igro(self, zmagovalec)`: konča igro in izpiše zamgovalca
* `prestavi_zeton(self, zeton, polje)`: prestavi žeton na izbrano polje
* `odstrani_zeton(self, zeton)`: odstrani žeton iz igralnega polja
* `klik_na_plosco(self, event)`: objektu igralca, ki je na potezi povemo, da je uporabnik kliknil na ploščo in vrnemo (koordinata, objekt), kjer je objekt žeton ali polje (odvisno na kaj je kliknil)
* `povleci_potezo(self, vrsta_poteze, zeton, polje=None)`: premaknemo žeton na polje, oziroma vzamemo žeton, odvisno od vrste poteze

#### Razreda `Clovek` in `Racunalnik`
Metode:
* `igraj(self)`: GUI pokliče metodo, ko je igralec na potezi
* `klik(self, koordinata, objekt)`: ko igralec klikne na ploščo, objekt ustrezno ukrepa (spremeni fazo poteze ali pokliče `povleci_potezo`), objekt je žeton ali polje na plošči
* `prekini(self)`: prekine razmišljanje objekta razreda `Alfabeta`

Razred `Racunalnik` ima še dodatno metodo:
* `preveri_potezo(self)`: vsakih 100 ms preveri, če je algoritem že izračunal potezo in pokliče `povleci_potezo`

#### Razred `Alfabeta`
Metode:
* `izracunaj_potezo(self, igra)`: poklice glavno metodo `alfabeta` in sporoči najboljšo potezo `GUI`-ju
* `vrednost_pozicije(self)`: izračuna vrednost trenutne pozicije s pomočjo `ocena_postavitve` v logiki igre
* `alfabeta(self, globina, alfa, beta, maksimiziramo)`: z algoritmom minimax izboljšanim z alfa-beta rezanjem izračuna najboljšo potezo do dane globine
