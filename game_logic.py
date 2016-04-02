IGRALEC_1 = 'igralec_1'
IGRALEC_2 = 'igralec_2'

class Igra():
    def __init__(self):
        # Naredi prazno igralno plosco.
        self.igralna_plosca = [None] * 24
        # na potezo postavi prvega igralca
        self.na_potezi = IGRALEC_1
        # na i-tem mestu v seznamu so sosedna polja i-tega polja na plosci
        self.sosedi = [[1, 9], [0, 2, 4], [1, 14], [4, 10], [1, 3, 5, 7], [4, 13], [7, 11], [4, 6, 8], [7, 12],
                       [0, 10, 21], [3, 9, 11, 18], [6, 10, 15], [8, 13, 17], [5, 12, 14, 20], [2, 13, 23], [11, 16],
                       [15, 17, 19], [12, 16], [10, 19], [16, 18, 20, 22], [13, 19], [9, 22], [19, 21, 23], [14, 22]]
        # polozaji vseh moznih trojk, ki lahko nastopijo na plosci
        self.trojke = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {9, 10, 11}, {12, 13, 14}, {15, 16, 17}, {18, 19, 20},
                       {21, 22, 23}, {0, 9, 21}, {3, 10, 18}, {6, 11, 15}, {1, 4, 7}, {16, 19, 22}, {8, 12, 17},
                       {5, 13, 20}, {2, 14, 23}]
        # v slovarju self.manjkajoca so kljuci pari sosednih polj na plosci,
        # vrednost pa je polje, ki manjka do zakljucene trojke
        # slovar bomo potrebovali pri oceni postavitve
        self.manjkajoca = {}
        for trojka in self.trojke:
            a, b, c = sorted(trojka)
            self.manjkajoca[(a, b)] = c
            self.manjkajoca[(a, c)] = b
            self.manjkajoca[(b, c)] = a


        # v seznamu self.zetoni ustreza indeks i zetonu i: "zacetek" - ni se vstopil v igro,
        # "izlocen" - je ze izlocen iz igre, n - nahaja se na igralni plosci na mestu n
        # indeksi 0-8 so za zetone igralca 1, ostali za zetone igralca 2
        self.zetoni = ["zacetek"] * 18
        # faza_igre 1 pomeni, da se zetoni sele postavljajo na plosco
        # faza_igre 2 pomeni, da se zetoni prestavljajo po plosci
        self.faza_igre = 1
        # pove, ce se je zakljucila poteza
        self.konec_poteze = False
        # pove, ce se je igra koncala
        self.konec_igre = False
        # pove, kdo je zmagovalec igre
        self.zmagovalec = None
        # vsebuje vse podatke o trenutnem stanju:
        # self.igralna_plosca, self.zetoni, self.na_potezi, self.faza_igre, self.konec_igre , self.zmagovalec in self.ponovljene
        self.zgodovina = []
        # vsebuje število ponovljenih potez
        self.ponovljene = 0

    def shrani_zgodovino(self):
        """Doda trenutno stanje igre v zgodovino."""
        self.zgodovina.append((self.igralna_plosca[:], self.zetoni[:], self.na_potezi, self.faza_igre, self.konec_igre, self.zmagovalec, self.ponovljene))

    def razveljavi(self):
        """Odstrani zadnji vnos iz zgodovine, ponastavi igro na prejsnje stanje."""
        (self.igralna_plosca, self.zetoni, self.na_potezi, self.faza_igre, self.konec_igre, self.zmagovalec, self.ponovljene) = self.zgodovina.pop()

    def kopija_igre(self):
        """Ustvari kopijo igre, ki jo racunalnik uporablja pri algoritmu alfa-beta, da ne spreminja dejanske plosce."""
        k = Igra()
        k.igralna_plosca = self.igralna_plosca[:]
        k.zetoni = self.zetoni[:]
        k.na_potezi = self.na_potezi
        k.faza_igre = self.faza_igre
        k.konec_igre = self.konec_igre
        k.zmagovalec = self.zmagovalec
        k.ponovljene = self.ponovljene
        k.zgodovina = self.zgodovina
        return k

    def veljavna_poteza(self, zeton, zeljeno_polje):
        """Dobi index zetona, fazo igre (1 ali 2) in index polja, kamor zelimo zeton postaviti."""
        # zeton je ze izlocen iz igre
        if self.zetoni[zeton] is "izlocen":
            return False
        # Preveri, ce zeton ne pripada igralcu.
        if self.na_potezi is IGRALEC_1 and zeton >= 9 or self.na_potezi is IGRALEC_2 and zeton < 9:
            return False
        # v fazi 1 preverjamo, ce je zeljeno_polje prazno in zeton se ni vstopil v igro
        if self.faza_igre == 1:
            return self.igralna_plosca[zeljeno_polje] is None and self.zetoni[zeton] is "zacetek"
        elif self.faza_igre == 2:
            if self.na_potezi is IGRALEC_1:
                # preverimo, ce ima igralec samo se 2 ali 3 aktivne zetone - potem lahko skace po plosci
                if self.zetoni[:9].count("izlocen") >= 6:
                    # preverimo, ce je zeljeno_polje prazno
                    return self.igralna_plosca[zeljeno_polje] is None
                else:
                    # igralec ne sme skakati - torej mora biti polje prazno in sosednje
                    return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in\
                                                                          self.sosedi[self.zetoni[zeton]]
            else:
                if self.zetoni[9:].count("izlocen") >= 6:
                    return self.igralna_plosca[zeljeno_polje] is None
                else:
                    return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in\
                                                                          self.sosedi[self.zetoni[zeton]]
        else:
            return False

    def veljavni_zakljucek(self, zeton):
        """Dobi indeks zetona, ki ga zelimo vzeti in preveri, ce je to veljavno."""
        # Spremenljivka mesto je mesto v seznamu, pri katerem se zacnejo zetoni nasprotnega igralca
        if self.na_potezi is IGRALEC_1:
            mesto = 9
        else:
            mesto = 0

        # Indeksi nasprotnikovih zetonov, ki se nahajajo na plosci (nimajo statusa "zacetek" ali "izlocen")
        izbire = [i for i in range(mesto, mesto + 9) if self.zetoni[i] not in ["izlocen", "zacetek"]]
        if zeton not in izbire:
            return False
        # ce zeton ni vsebovan v trojki, ga lahko vzamemo
        elif not self.nova_trojka(zeton):
            return True
        else:
            for i in izbire:
                if not self.nova_trojka(i):
                    return False
        # ce bi obstajal nasprotnikov zeton, ki ni v trojki, bi pri prejsnjem else stavku ze vrnili False
        # torej so vsi naprotnikovi zetoni v trojkah - lahko vzamemo poljubnega
        return True

    def odigraj_potezo(self, zeton, polje):
        """Sprejme indeks zetona in polje, kamor ga zelimo prestaviti, ter odigra potezo.
        Privzamemo, da je poteza veljavna - veljavnost bo preveril objekt razreda Clovek ali Racunalnik, preden poklice to metodo"""
        self.shrani_zgodovino()
        if self.zetoni[zeton] is "zacetek":
            # zeton prvic vstopi v igro
            self.zetoni[zeton] = polje
            self.igralna_plosca[polje] = zeton
        else:
            # zeton premikamo po plosci
            self.igralna_plosca[self.zetoni[zeton]] = None
            self.igralna_plosca[polje] = zeton
            self.zetoni[zeton] = polje
        if not self.nova_trojka(zeton):
            # ni nastala nova trojka
            self.zakljucek_poteze(zeton=None)

    def nova_trojka(self, zeton):
        """Preveri, ce obstaja trojka, ki vsebuje dani zeton"""
        # v seznamu so vse trojke, ki vsebujejo pozicijo, na kateri se nahaja zeton
        moznosti = [trojka for trojka in self.trojke if self.zetoni[zeton] in trojka]
        # preverimo, ce potencialna trojka zares vsebuje vse 3 zetone istega igralca
        # zeton pripada igralcu 1
        if zeton < 9:
            for moznost in moznosti:
                if moznost <= set(self.zetoni[:9]):
                    return True
            return False
        # zeton pripada igralcu 2
        if zeton >= 9:
            for moznost in moznosti:
                if moznost <= set(self.zetoni[9:]):
                    return True
            return False

    def zakljucek_poteze(self, zeton=None):
        """Sprejme indeks zetona, ki ga zelimo vzeti in ustrezno odigra - veljavnost te poteze bo ze prej preveril objekt razreda Clovek ali Racunalnik.
        Privzeti parameter None pove, da ne bomo vzeli nobenega zetona."""
        if zeton is not None:
            self.shrani_zgodovino()
            self.igralna_plosca[self.zetoni[zeton]] = None
            self.zetoni[zeton] = "izlocen"
        # spremenimo igralca, ki je na potezi
        if self.na_potezi is IGRALEC_1:
            self.na_potezi = IGRALEC_2
        else:
            self.na_potezi = IGRALEC_1
        # povemo, da se je poteza zakljucila
        self.konec_poteze = True
        # poklicemo stanje igre
        self.stanje_igre()

    def veljavne_poteze(self):
        """Vrne seznam parov (i, n), kjer je i indeks zetona, ki ga lahko prestavimo, in n polje na plosci, kamor ga
        lahko prestavimo, da bo poteza veljavna.
        Dokler zetone samo postavljamo na plosco, lahko postavimo samo tistega z najnizjim indeksom (vse ostale poteze so enakovredne in jih lahko izpustimo)"""
        # Spremenljivka mesto je mesto v seznamu, pri katerem se zacnejo zetoni danega igralca
        if self.na_potezi is IGRALEC_1:
            mesto = 0
        else:
            mesto = 9

        prazna_polja = [i for i in range(24) if self.igralna_plosca[i] is None]
        poteze = []
        # obstajajo zetoni, ki se niso bili postavljeni na plosco
        if self.zetoni[mesto:(mesto + 9)].count("zacetek") != 0:
            najnizji_index = self.zetoni[mesto:(mesto + 9)].index("zacetek") + mesto
            for polje in prazna_polja:
                poteze.append((najnizji_index, polje))
            return poteze
        # vsi zetoni se ze nahajajo na plosci (nobeden nima statusa "zacetek")
        # igralec ima 3 zetone ali manj - lahko skace po plosci
        elif self.zetoni[mesto:(mesto + 9)].count('izlocen') >= 6:
            for zeton in range(mesto, mesto + 9):
                # preverimo, ce je zeton se v igri
                if self.zetoni[zeton] != "izlocen":
                    for polje in prazna_polja:
                        poteze.append((zeton, polje))
            return poteze
        # igralec se ne sme skakati po plosci
        else:
            for zeton in range(mesto, mesto + 9):
                # preverimo, ce je zeton se v igri
                if self.zetoni[zeton] != "izlocen":
                    # zeton lahko prestavimo le na prazno sosedno polje
                    for sosed in self.sosedi[self.zetoni[zeton]]:
                        if sosed in prazna_polja:
                            poteze.append((zeton, sosed))
            return poteze

    def veljavni_zakljucki(self):
        """Vrne seznam indeksov zetonov, ki jih lahko vzamemo s plosce"""
        return [indeks for indeks in range(18) if self.veljavni_zakljucek(indeks)]

    def stanje_igre(self):
        """Ustrezno spremeni atribute faza_igre, konec_igre, ponovljene in zmagovalec po koncu vsake poteze"""
        # igralec na potezi nima vec veljavnih potez ali pa sta mu ostala samo se 2 zetona
        if self.na_potezi is IGRALEC_1 and (self.zetoni[:9].count("izlocen") >= 7 or len(self.veljavne_poteze()) == 0):
            self.konec_igre = True
            self.zmagovalec = IGRALEC_2
        if self.na_potezi is IGRALEC_2 and (self.zetoni[9:].count("izlocen") >= 7 or len(self.veljavne_poteze()) == 0):
            self.konec_igre = True
            self.zmagovalec = IGRALEC_1
        # ce smo vse zetone ze polozili na plosci se pricne premikanje zetonov po plosci - druga faza igre
        if self.zetoni.count("zacetek") == 0:
            self.faza_igre = 2
        # med prvo fazo igre se poteze ne morejo ponavljati
        if self.faza_igre == 2:
            # pogledamo, ce se je poteza ponovila
            # vmes smo 2krat shranili odigrano potezo in 2krat odigrani zakljucek (za nas in za nasprotnika)
            # torej moramo v zgodovino pogledati za 4 nazaj, da dobimo plosco kot je izgledala, ko smo bli prejsnjic na vrsti
            if self.zgodovina[-4][0] == self.igralna_plosca:
                self.ponovljene += 1
            # v nasprotnem primeru resetiramo stevec ponovljenih potez
            else:
                self.ponovljene = 0
        # ce se je dvakrat ponovil popolnoma isti cikel (torej 2 poteze od vsakega igralca, skupno 4), je igra neodlocena
        if self.ponovljene == 4:
            self.konec_igre = True
            self.zmagovalec = "neodloceno"

    def ocena_postavitve(self):
        """Vrne nabor (r1, r2, r3, r4, r5, r6, r7), ki predstavlja koeficiente v utezeni vsoti pri izracunu vrednosti pozicije"""
        # r1 je razlika med stevilom trojk igralca 1 in igralca 2
        # r2 je razlika med stevilom blokiranih zetonov igralca 1 in igralca 2
        # r3 je razlika med stevilom zetonov igralca 1 in igralca 2
        # r4 je razlika med stevilom "2 pieces configuration" igralca 1 in igralca 2
        # "2 pieces configuration" - dva zetona istega igralca sta v potencialni trojki, tretje mesto pa je se prazno
        # r5 je razlika med stevilom "3 pieces configuration" igralca 2 in igralca 2
        # "3 pieces configuration" - dva "2 pieces configuration" z nepraznim presekom (tvorita 2 odprti dvojki, torej vsaj ene nasprotnik ne bo mogel zapreti)
        # r6 je razlika med stevilom zavzetih krizisc igralca 1 in igralca 2
        # r7 je razlika med stevilom odprtih trojk igralca 1 in igralca 2

        r1, r2, r3, r4, r5, r6, r7 = 0, 0, 0, 0, 0, 0, 0
        # naredimo mnozici mest (pozicij na plosci), na katerih so zetoni igralca 1 in igralca 2
        zetoni1 = {x for x in self.zetoni[:9] if x not in ['izlocen', 'zacetek']}
        zetoni2 = {x for x in self.zetoni[9:] if x not in ['izlocen', 'zacetek']}
        # razlika med zetoni igralca 1 in igralca 2 je enaka razliki izlocenih zetonov igralca 2 in igralca 1
        r3 = self.zetoni[9:].count('izlocen') - self.zetoni[:9].count('izlocen')

        # indeksi krizisc so 4, 10, 13 in 19
        # prestejemo koliko krizisc ima v lasti posamezni igralec
        for krizisce in [4, 10, 13, 19]:
            if krizisce in zetoni1:
                r6 += 1
            elif krizisce in zetoni2:
                r6 -= 1

        # v seznam dvojke1 bomo dodajali mnozice dveh zetonov igralca 1, ki tvorita "2 pieces configuration"
        # v seznam dvojke2 bomo dodajali mnozice dveh zetonov igralca 2, ki tvorita "2 pieces configuration"
        dvojke1 = []
        dvojke2 = []

        # pregledamo celoten seznam moznih trojk
        for a, b, c in self.trojke:
            # spremenljivka prvi steje stevilo zetonov igralca 1 v trojki
            prvi = 0
            # mnozica mest zetonov igralca 1 v trojki
            mesta1 = set()
            # drugi in mesta2 sta definirana analogno za igralca 2
            drugi = 0
            mesta2 = set()
            if a in zetoni1:
                prvi += 1
                mesta1.add(a)
            if a in zetoni2:
                drugi += 1
                mesta2.add(a)
            if b in zetoni1:
                prvi += 1
                mesta1.add(b)
            if b in zetoni2:
                drugi += 1
                mesta2.add(b)
            if c in zetoni1:
                prvi += 1
                mesta1.add(c)
            if c in zetoni2:
                drugi += 1
                mesta2.add(c)
            # ce celotna trojka pripada igralcu 1, povecamo r1
            if prvi == 3:
                r1 += 1
            # ce celotna trojka pripada igralcu 2, zmanjsamo r1
            elif drugi == 3:
                r1 -= 1
            # ce 2 zetona pripadata igralcu 1, tretje mesto v trojki pa je se prazno, povecamo r4 in mesta1 dodamo v mnozico dvojk igralca 1
            elif prvi == 2 and drugi == 0:
                r4 += 1
                dvojke1.append(mesta1)
            # ce 2 zetona pripadata igralcu 2, tretje mesto v trojki pa je se prazno, zmanjsamo r4 in mesta2 dodamo v mnozico dvojk igralca 2
            elif prvi == 0 and drugi == 2:
                dvojke2.append(mesta2)
                r4 -= 1

        # med vsemi dvojkami igralca 1 poiscemo tiste, ki ustrezajo pogoju za 
        for dvojka1 in dvojke1:
            for dvojka2 in dvojke1:
                # v preseku mora biti natanko en element - ce sta 2, pomeni, da gledamo presek dvojke s sabo"
                if len(dvojka1 & dvojka2) == 1:
                    r5 += 1
        # med vsemi dvojkami igralca 2 poiscemo tiste, ki ustrezajo pogoju za "3 pieces configuration"
        for dvojka1 in dvojke2:
            for dvojka2 in dvojke2:
                if len(dvojka1 & dvojka2) == 1:
                    r5 -= 1
        # vse "3 pieces configuration" smo steli dvakrat, zato skupno stevilo delimo z 2
        r5 //= 2

        # med vsemi dvojkami igralca 1 poiscemo tiste, ki jih lahko z enim premikom zetona zapremo do trojke - odprte trojke
        for dvojka in dvojke1:
            # pogledamo katero polje manjka dvojki do trojke
            manjkajoce_polje = self.manjkajoca[tuple(sorted(dvojka))]
            # med vsemi sosedi manjkajocega polja izberemo samo tiste, ki pripadajo igralcu 1
            sosedi = set(self.sosedi[manjkajoce_polje]) & zetoni1
            # izmed teh sosedov so nekateri ze v tej dvojki - pogledamo ce je vsaj en tak sosed, ki ni del te dvojke (da bo lahko dokoncal trojko)
            if len(sosedi - dvojka) >= 1:
                r7 += 1
        # med vsemi dvojkami igralca 2 poiscemo tiste, ki jih lahko z enim premikom zetona zapremo do trojke - odprte trojke
        for dvojka in dvojke2:
            manjkajoce_polje = self.manjkajoca[tuple(sorted(dvojka))]
            sosedi = set(self.sosedi[manjkajoce_polje]) & zetoni2
            if len(sosedi - dvojka) >= 1:
                r7 -= 1

        # kateri zetoni igralca 1 so blokirani
        for zeton in zetoni1:
            # zeton je blokiran, ce so na vseh sosednih poljih ze drugi zetoni
            if set(self.sosedi[zeton]) <= (zetoni2 | zetoni1):
                r2 -= 1
        # kateri zetoni igralca 2 so blokirani
        for zeton in zetoni2:
            if set(self.sosedi[zeton]) <= (zetoni2 | zetoni1):
                r2 += 1

        return (r1, r2, r3, r4, r5, r6, r7)
