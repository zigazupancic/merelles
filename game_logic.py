IGRALEC_1 = 'igralec_1'
IGRALEC_2 = 'igralec_2'

class Igra():
    def __init__(self):
        #naredi prazno igralco plosco
        self.igralna_plosca = [None] * 24
        #na potezo postavi prvega igralca
        self.na_potezi = IGRALEC_1
        #na i-tem mestu v seznamu so sosedna polja i-tega polja na plosci
        self.sosedi = [[1, 9], [0, 2, 4], [1, 14], [4, 10], [1, 3, 5, 7], [4, 13], [7, 11], [4, 6, 8], [7, 12],
                       [0, 10, 21], [3, 9, 11, 18], [6, 10, 15], [8, 13, 17], [5, 12, 14, 20], [2, 13, 23], [11, 16],
                       [15, 17, 19], [12, 16], [10, 19], [16, 18, 20, 22], [13, 19], [9, 22], [19, 21, 23], [14, 22]]
        #polozaji vseh moznih trojk, ki lahko nastopijo na plosci
        self.trojke = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {9, 10, 11}, {12, 13, 14}, {15, 16, 17}, {18, 19, 20},
                       {21, 22, 23}, {0, 9, 21}, {3, 10, 18}, {6, 11, 15}, {1, 4, 7}, {16, 19, 22}, {8, 12, 17},
                       {5, 13, 20}, {2, 14, 23}]
        #v seznamu self.zetoni ustreza indeks i zetonu i: None - ni se vstopil v igro,
        #False - je ze izlocen iz igre, n - nahaja se na igralni plosci na mestu n
        #indeksi 0-8 so za zetone igralca 1, ostali za zetone igralca 2
        self.zetoni = [None] * 18
        #faza_igre 1 pomeni, da se zetoni sele postavljajo na plosco
        #faza_igre 2 pomeni, da se zetoni prestavljajo po plosci
        self.faza_igre = 1
        #pove, ce se je zakljucila poteza
        self.konec_poteze = False
        #pove, ce se je igra koncala
        self.konec_igre = False
        #pove, kdo je zmagovalec igre
        self.zmagovalec = None

    def veljavna_poteza(self, zeton, zeljeno_polje):
        """Dobi index zetona, fazo igre (1-2) in index polja kamor zelimo zeton postaviti"""
        if self.zetoni[zeton] is False:
            return False
        if self.na_potezi is IGRALEC_1 and zeton >= 9 or self.na_potezi is IGRALEC_2 and zeton < 9:
            return False
        if self.faza_igre == 1:
            return self.igralna_plosca[zeljeno_polje] is None and self.zetoni[zeton] is None
        elif self.faza_igre == 2:
            if self.na_potezi is IGRALEC_1:
                # preverimo, ce ima igralec samo se 2 ali 3 aktivne zetone - potem lahko skace po plosci
                if self.zetoni[:9].count(False) >= 6:
                    return self.igralna_plosca[zeljeno_polje] is None
                else:
                    return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in\
                                                                          self.sosedi[self.zetoni[zeton]]
            else:
                if self.zetoni[9:].count(False) >= 6:
                    return self.igralna_plosca[zeljeno_polje] is None
                else:
                    return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in\
                                                                          self.sosedi[self.zetoni[zeton]]
        else:
            return False

    def veljavni_zakljucek(self, zeton):
        """Dobi indeks zetona, ki ga zelimo vzeti in preveri, ce je to veljavno"""
        if self.na_potezi is IGRALEC_1:
            #indeksi nasprotnikovih zetonov, ki se nahajajo na plosci (nimajo statusa False ali None)
            izbire = [i for i in range(9, 18) if self.zetoni[i] not in [False, None]]
            if zeton not in izbire:
                return False
            ali_so_v_trojki = [self.nova_trojka(i) for i in izbire]
            #ce so vsi v trojkah, si lahko izbere kateregakoli s plosce
            if ali_so_v_trojki.count(True) == len(ali_so_v_trojki):
                return True
            else:
                return not self.nova_trojka(zeton)
        else:
            #indeksi nasprotnikovih zetonov, ki se nahajajo na plosci (nimajo statusa False ali None)
            izbire = [i for i in range(9) if self.zetoni[i] not in [False, None]]
            if zeton not in izbire:
                return False
            ali_so_v_trojki = [self.nova_trojka(i) for i in izbire]
            #ce so vsi v trojkah, si lahko izbere kateregakoli s plosce
            if ali_so_v_trojki.count(True) == len(ali_so_v_trojki):
                return True
            else:
                return not self.nova_trojka(zeton)
    
    def odigraj_potezo(self, zeton, polje):
        """Sprejme indeks zetona in polje, kamor ga zelimo prestaviti.
        Privzamemo, da je poteza veljavna - veljavnost bo preveril GUI, preden poklice to metodo"""
        if self.zetoni[zeton] is None:
            #zeton prvic vstopi v igro
            self.zetoni[zeton] = polje
            self.igralna_plosca[polje] = zeton
        else:
            #zeton premikamo po plosci
            self.igralna_plosca[self.zetoni[zeton]] = None
            self.igralna_plosca[polje] = zeton
            self.zetoni[zeton] = polje
        if not self.nova_trojka(zeton):
            #ni nastala nova trojka
            self.zakljucek_poteze(zeton=None)

    def nova_trojka(self, zeton):
        """Preveri, ce obstaja trojka, ki vsebuje dani zeton"""
        moznosti = [trojka for trojka in self.trojke if self.zetoni[zeton] in trojka]
        if self.na_potezi is IGRALEC_1:
            for moznost in moznosti:
                if moznost <= set(self.zetoni[:9]):
                    return True
            return False
        if self.na_potezi is IGRALEC_2:
            for moznost in moznosti:
                if moznost <= set(self.zetoni[9:]):
                    return True
            return False

    def zakljucek_poteze(self, zeton=None):
        """Sprejme indeks zetona, ki ga zelimo vzeti - veljavnost te poteze bo ze prej preveril GUI.
        Privzeti parameter None pove, da ne bomo vzeli nobenega zetona"""
        if zeton is not None:
            self.igralna_plosca[self.zetoni[zeton]] = None
            self.zetoni[zeton] = False
        #spremenimo igralca
        if self.na_potezi is IGRALEC_1:
            self.na_potezi = IGRALEC_2
        else:
            self.na_potezi = IGRALEC_1
        #povemo, da se je poteza zakljucila
        self.konec_poteze = True
        #poklicemo stanje igre
        self.stanje_igre()
    
    def veljavne_poteze(self):
        """Vrne seznam parov (i, n), kjer je i indeks zetona, ki ga lahko prestavimo, in n polje na plosci, kamor ga
        lahko prestavimo, da bo poteza veljavna.
        Dokler zetone samo postavljamo na plosco, lahko postavimo samo tistega z najnizjim indeksom"""
        prazna_polja = [i for i in range(24) if self.igralna_plosca is None]
        if self.na_potezi is IGRALEC_1:
            poteze = []
            #obstajajo zetoni, ki se niso bili postavljeni na plosco
            if self.zetoni[:9].count(None) != 0:
                najnizji_index = self.zetoni[:9].index(None)
                for polje in prazna_polja:
                    poteze.append((najnizji_index, polje))
                return poteze
            #vsi zetoni se ze nahajajo na plosci (nobeden nima statusa None)
            else:
                for i in range(9):
                    #zeton (oznacuje pozicijo na plosci) je se v igri
                    if self.zetoni[i] != False:
                        for sosed in self.sosedi[self.zetoni[i]]:
                            if sosed in prazna_polja:
                                poteze.append((i, sosed))
                return poteze
        elif self.na_potezi is IGRALEC_2:
            poteze = []
            #obstajajo zetoni, ki se niso bili postavljeni na plosco
            if self.zetoni[9:].count(None) != 0:
                najnizji_index = self.zetoni[9:].index(None) + 9
                for polje in prazna_polja:
                    poteze.append((najnizji_index, polje))
                return poteze
            #vsi zetoni se ze nahajajo na plosci (nobeden nima statusa None)
            else:
                for i in range(9, 18):
                    #zeton (oznacuje pozicijo na plosci) je se v igri
                    if self.zetoni[i] != False:
                        for sosed in self.sosedi[self.zetoni[i]]:
                            if sosed in prazna_polja:
                                poteze.append((i, sosed))
                return poteze

    def veljavni_zakljucki(self):
        """Vrne seznam indeksov zetonov, ki jih lahko vzamemo s plosce"""
        return [indeks for indeks in range(24) if self.veljavni_zakljucek(indeks)]

    def stanje_igre(self):
        """Ustrezno spremeni atribute faza_igre, konec_igre in zmagovalec"""
        #igralec na potezi nima vec veljavnih potez ali pa sta mu ostala samo se 2 zetona
        if self.na_potezi is IGRALEC_1 and (self.zetoni[:9].count(False) >= 7 or len(self.veljavne_poteze()) == 0):
            self.konec_igre = True
            self.zmagovalec = IGRALEC_2
        if self.na_potezi is IGRALEC_2 and (self.zetoni[9:].count(False) >= 7 or len(self.veljavne_poteze()) == 0):
            self.konec_igre = True
            self.zmagovalec = IGRALEC_1
        #vse zetone smo se polozili na plosco - pricne se premikanje zetonov po plosci
        if self.zetoni.count(None) == 0:
            self.faza_igre = 2

