"""Glavni del programa Merelles."""
import tkinter as tk     # Knjižnica za grafični vmesnik.
import game_logic        # Knjižnica za logiko igre.
import threading
import time
import random

class GUI():
    """Razred grafičnega vmesnika, ki izriše glavno okno komunicira med uporabnikom in igro."""

    # Velikost delcka plosce.
    VELIKOST_ODSEKA = 100

    # Barve žetonov
    BARVA_IGRALEC_1 = "red4"
    BARVA_IGRALEC_1_PRITISNJEN = "red"
    BARVA_IGRALEC_2 = "green4"
    BARVA_IGRALEC_2_PRITISNJEN = "lawn green"

    def __init__(self, master):
        """Ustvari menije in podmenije, izriše igralno ploščo in začne igro s privzetimi nastavitvami.
        :param master: glavno okno igre
        """

        # Nastavitev atributov
        self.master = master                     # Glavno okno.
        self.igralec_1 = None                    # Ob začetku nove igra, bo to objekt razreda Oseba ali Računalnik.
        self.igralec_2 = None                    # Ob začetku nove igra, bo to objekt razreda Oseba ali Računalnik.
        self.igra = None                         # Ob začetku nove igra, bo to objekt razreda Igra.
        self.ime_1 = "Rdeči"                     # Privzeto ime prvega igralca.
        self.ime_2 = "Zeleni"                    # Privzeto ime drugega igralca.
        self.about = None                        # Okno za podatke o igri, ko ni odprto je None.
        self.help = None                         # Okno za pomoč pri igranju igre, ko ni odprto je None.

        self.master.resizable(width=False, height=False)         # Velikosti okna ni mogoče spreminjati
        # Glavni meni
        menu = tk.Menu(master)
        master.config(menu=menu)

        # Podmeni Igra
        menu_igra = tk.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra", command=self.izbira_nove_igre)
        menu_igra.add_command(label="Izhod", command=master.destroy)

        # Podmeni Pomoč
        menu_pomoc = tk.Menu(menu)
        menu.add_cascade(label="Pomoč", menu=menu_pomoc)
        menu_pomoc.add_command(label="Kako igrati", command=self.pomoc)
        menu_pomoc.add_command(label="O igri", command=self.o_igri)

        # Napis igre in polje za informacije
        self.napis = tk.StringVar(self.master, value="Na potezi je {}.".format(self.ime_1))
        tk.Label(self.master, textvariable=self.napis, font=("Helvetica", 20)).grid(row=0, column=0)

        # Ustvari platno plosca in ga postavi v okno
        d = GUI.VELIKOST_ODSEKA
        self.plosca = tk.Canvas(master, width=12 * d, height=7.5 * d)
        self.plosca.grid(row=1, column=0)

        # Ozadje plošče
        self.plosca.create_rectangle(2.5 * d, 0.25 * d, 9.5 * d, 7.25 * d, fill="beige", width=0)

        # Povezava koordinat platna in koordinat polj na plosci
        self.koordinate = {(3 * d, 0.75 * d): 0, (6 * d, 0.75 * d): 1, (9 * d, 0.75 * d): 2, (4 * d, 1.75 * d): 3,
                           (6 * d, 1.75 * d): 4, (8 * d, 1.75 * d): 5, (5 * d, 2.75 * d): 6, (6 * d, 2.75 * d): 7,
                           (7 * d, 2.75 * d): 8, (3 * d, 3.75 * d): 9, (4 * d, 3.75 * d): 10, (5 * d, 3.75 * d): 11,
                           (7 * d, 3.75 * d): 12, (8 * d, 3.75 * d): 13, (9 * d, 3.75 * d): 14, (5 * d, 4.75 * d): 15,
                           (6 * d, 4.75 * d): 16, (7 * d, 4.75 * d): 17, (4 * d, 5.75 * d): 18, (6 * d, 5.75 * d): 19,
                           (8 * d, 5.75 * d): 20, (3 * d, 6.75 * d): 21, (6 * d, 6.75 * d): 22, (9 * d, 6.75 * d): 23}

        # igralna plošča
        # ---------------------------------------------------------
        # Okvir
        self.plosca.create_rectangle(3 * d, 0.75 * d, 9 * d, 6.75 * d, width=0.06 * d)
        self.plosca.create_rectangle(4 * d, 1.75 * d, 8 * d, 5.75 * d, width=0.06 * d)
        self.plosca.create_rectangle(5 * d, 2.75 * d, 7 * d, 4.75 * d, width=0.06 * d)

        self.plosca.create_line(6 * d, 0.75 * d, 6 * d, 2.75 * d, width=0.06 * d)
        self.plosca.create_line(6 * d, 4.75 * d, 6 * d, 6.75 * d, width=0.06 * d)
        self.plosca.create_line(3 * d, 3.75 * d, 5 * d, 3.75 * d, width=0.06 * d)
        self.plosca.create_line(7 * d, 3.75 * d, 9 * d, 3.75 * d, width=0.06 * d)

        # Polja
        for (x, y) in self.koordinate:
            self.plosca.create_oval(x - 0.15 * d, y - 0.15 * d, x + 0.15 * d, y + 0.15 * d, fill="black")
        # ---------------------------------------------------------

        # Seznam indeksov žetonov, ki so na plošči, kot jih vrne create_oval.
        self.narisani_zetoni = []

        # Ob kliku na ploščo se pokliče metoda klik_na_plosco.
        self.plosca.bind("<Button-1>", self.klik_na_plosco)

        # Začne novo igro s privzetimi nastavitvami.
        self.nova_igra(Clovek, Clovek)

    def o_igri(self):
        """Ustvari okno s podatki o igri."""

        def preklici():
            """Pomožna funkcija, ki zapre okno in nastavi atribut self.about na None."""
            self.about.destroy()
            self.about = None

        # Preveri, če je okno že ustvarjeno, če je ga da na vrh in se vrne.
        if self.about is not None:
            self.about.lift()
            return

        # Ustvari okno z informacijami o igri.
        self.about = tk.Toplevel()
        self.about.title("O igri")
        self.about.resizable(width=False, height=False)
        self.about.protocol("WM_DELETE_WINDOW", preklici)

        self.about.grid_columnconfigure(0, minsize=400)
        self.about.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        self.about.grid_rowconfigure(2, minsize=80)             # Nastavitev minimalne višine druge vrstice

        tk.Label(self.about, text="Merelles (Mlin) je strateška igra za dva igralca, \n ki izvira iz Rimskega imperija."
                                  "\nObstaja več različic igre (z različnim \n"
                                  "številom žetonov in povezav na plošči).", justify="left").grid(row=1, column=0)
        tk.Label(self.about, text="O igri Merelles (Mlin)", font=("Helvetica", 20)).grid(row=0, column=0)
        tk.Label(self.about, text="Avtorja aplikacije: Žiga Zupančič in Juš Kosmač \n Licenca: MIT \n "
                                  "Aplikacija ustvarjena za Programiranje 2 (FMF) - 2016.",
                 justify="left").grid(row=2, column=0)

    def pomoc(self):
        """Ustvari okno s pomočjo pri igranju igre."""

        def preklici():
            """Pomožna funkcija, ki zapre okno in nastavi atribut self.help na None."""
            self.help.destroy()
            self.help = None

        # Preveri, če je okno že ustvarjeno, če je ga da na vrh in se vrne.
        if self.help is not None:
            self.help.lift()
            return

        # Ustvari okno z informacijami o igri.
        self.help = tk.Toplevel()
        self.help.title("Kako igrati")
        self.help.resizable(width=False, height=False)
        self.help.protocol("WM_DELETE_WINDOW", preklici)

        self.help.grid_columnconfigure(0, minsize=600)
        self.help.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        self.help.grid_rowconfigure(2, minsize=80)             # Nastavitev minimalne višine druge vrstice

        tk.Label(self.help, text="Navodila za igranje igre Merelles (Mlin)", font=("Helvetica", 20)).grid(row=0, column=0)

        tk.Label(self.help, text="Vsak igralec na začetku igre prejme 9 žetonov svoje barve, \n"
                                 "ki jih nato z nasprotnikom v prvi fazi igre izmenično postavljata \n"
                                 "na igralno ploščo. Ko igralec v ravno vrsto postavi tri svoje \n"
                                 "žetone, nasprotniku vzame žeton z igralne plošče. Ko oba igralca \n"
                                 "postavita svojih 9 žetonov na igralno ploščo, se začne druga faza \n"
                                 "igre, v kateri se lahko žetoni premikajo na sosednja polja. Igralca \n"
                                 "s tem skušata poravnati svoje tri žetone v vrsto, da lahko jemljeta \n"
                                 "žeton nasprotniku. Izgubi igralec, ki ima manj kot tri žetone, ali \n"
                                 "nima več dovoljene poteze. Ko ima igralec le še tri žetone, \n"
                                 "jih lahko poljubno premika po igralni plošči, torej skače. \n"
                                 "Če se trikrat ponovi ista poteza, je rezultat neodločen.",
                 justify="left").grid(row=1, column=0)

    def izbira_nove_igre(self):
        """Ustvari okno za izbiro nastavitev nove igre (če ne obstaja) ter začne novo igro, z izbranimi nastavitvami."""

        def ustvari_igro():
            """Pomožna funkcija, ki ustvari novo igro, nastavi ime igralcev ter zapre okno za izbiro nastavitev."""
            self.ime_1 = ime_1.get()
            self.ime_2 = ime_2.get()
            if igralec_1_clovek.get():
                igralec_1 = Clovek
            else:
                igralec_1 = Racunalnik
            if igralec_2_clovek.get():
                igralec_2 = Clovek
            else:
                igralec_2 = Racunalnik
            self.nova_igra(igralec_1, igralec_2, izbrana_tezavnost.get())
            new_game.destroy()

        # Ustvari novo okno za izbiro nastavitev nove igre.
        new_game = tk.Toplevel()
        new_game.grab_set()                                   # Postavi fokus na okno in ga obdrži
        new_game.title("Merelles - Nova igra")                # Naslov okna
        new_game.resizable(width=False, height=False)         # Velikosti okna ni mogoče spreminjati

        new_game.grid_columnconfigure(0, minsize=120)         # Nastavitev minimalne širine ničtega stolpca
        new_game.grid_columnconfigure(2, minsize=150)         # Nastavitev minimalne širine drugega stolpca
        new_game.grid_rowconfigure(0, minsize=80)             # Nastavitev minimalne višine ničte vrstice
        new_game.grid_rowconfigure(5, minsize=70)             # Nastavitev minimalne višine pete vrstice
        new_game.grid_rowconfigure(9, minsize=80)             # Nastavitev minimalne višine devete vrstice

        tk.Label(new_game, text="Nastavitve nove igre", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=4)

        # Nastavitve težavnosti
        # ---------------------------------------------------------
        tk.Label(new_game, text="Izberite težavnost:").grid(row=1, column=1, sticky="W")
        tezavnosti = [("Težko", 5), ("Srednje", 4), ("Lahko", 2)]  # Možne težavnosti
        izbrana_tezavnost = tk.IntVar()                            # Spremenljivka kamor shranimo izbrano težavnost
        izbrana_tezavnost.set(4)                                   # Nastavitev privzete vrednosti

        # Ustvari radijske gumbe za izbrio težavnosti:
        for vrstica, (besedilo, vrednost) in enumerate(tezavnosti):
            tk.Radiobutton(new_game, text=besedilo, variable=izbrana_tezavnost, value=vrednost, width=10,
                           anchor="w").grid(row=vrstica + 2, column=1)
        # ---------------------------------------------------------

        # Nastavitve igralcev
        # ---------------------------------------------------------
        tk.Label(new_game, text="IGRALEC 1", font=("Helvetica", 13)).grid(row=5, column=0, sticky="E")
        tk.Label(new_game, text="IGRALEC 2", font=("Helvetica", 13)).grid(row=5, column=2, sticky="E")
        tk.Label(new_game, text="Vrsta igralca:").grid(row=6, column=0, rowspan=2, sticky="E")
        tk.Label(new_game, text="Vrsta igralca:").grid(row=6, column=2, rowspan=2, sticky="E")

        igralec_1_clovek = tk.BooleanVar()                         # Spremenljivka kamor shranimo vrsto prvega igralca
        igralec_1_clovek.set(True)                                 # Privzeta vrednost vrste prvega igralca
        igralec_2_clovek = tk.BooleanVar()                         # Spremenljivka kamor shranimo vrsto drugega igralca
        igralec_2_clovek.set(True)                                 # Privzeta vrednost vrste drugega igralca
        igralci = [("Človek", True, igralec_1_clovek, 6, 1), ("Računalnik", False, igralec_1_clovek, 7, 1),
                   ("Človek", True, igralec_2_clovek, 6, 3), ("Računalnik", False, igralec_2_clovek, 7, 3)]

        # Ustvari radijske gumbe za izbiro vrste igralcev
        for besedilo, vrednost, spremenljivka, vrstica, stolpec in igralci:
            tk.Radiobutton(new_game, text=besedilo, variable=spremenljivka, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica, column=stolpec)

        tk.Label(new_game, text="Ime igralca:").grid(row=8, column=0, sticky="E")
        tk.Label(new_game, text="Ime igralca:").grid(row=8, column=2, sticky="E")

        ime_1 = tk.Entry(new_game, font="Helvetica 12", width=10)  # Vnosno polje za ime prvega igralca
        ime_1.grid(row=8, column=1)
        ime_1.insert(0, self.ime_1)                                     # Privzeto ime prvega igralca
        ime_2 = tk.Entry(new_game, font="Helvetica 12", width=10)  # Vnosno polje za ime drugega igralca
        ime_2.grid(row=8, column=3)
        ime_2.insert(0, self.ime_2)                                     # Privzeto ime drugega igralca
        # ---------------------------------------------------------

        # Gumba za začetek nove igre in preklic
        tk.Button(new_game, text="Prekliči", width=20, height=2,
                  command=lambda: new_game.destroy()).grid(row=9, column=0, columnspan=3, sticky="E")
        tk.Button(new_game, text="Začni igro", width=20, height=2,
                  command=lambda: ustvari_igro()).grid(row=9, column=3, columnspan=3, sticky="E")

    def nova_igra(self, igralec_1, igralec_2, tezavnost=2):
        """Ustvari novo igro s težavnostjo tezavnost in objekta razredov igralec_1 in igralec_2."""

        d = GUI.VELIKOST_ODSEKA

        if self.igralec_1 is not None:
            self.igralec_1.prekini()
        if self.igralec_2 is not None:
            self.igralec_2.prekini()

        # Ustvari objekte razredov igralec_1 in igralec_2.
        self.igralec_1 = igralec_1(self, tezavnost)
        self.igralec_2 = igralec_2(self, tezavnost)

        # Ustvari objekt razreda Igra() iz logike igre.
        self.igra = game_logic.Igra()

        # Pobirisi zetone, ki so ostali na plosci.
        self.plosca.delete("zeton")
        self.plosca.delete("pojeden")

        # Nariši žetone obeh igralcev.
        self.narisani_zetoni = []
        for zeton in range(5):
            self.narisani_zetoni.append(self.plosca.create_oval(
                0.325*d, 6*d - d*zeton, 0.925*d, 6.6*d - d*zeton, fill=GUI.BARVA_IGRALEC_1, tags="zeton",
                state="normal", width=0.03*d))

        for zeton in range(4):
            self.narisani_zetoni.append(self.plosca.create_oval(
                1.575*d, 6*d - d*zeton, 2.175*d, 6.6*d - d*zeton, fill=GUI.BARVA_IGRALEC_1, tags="zeton",
                state="normal", width=0.03*d))

        for zeton in range(5):
            self.narisani_zetoni.append(self.plosca.create_oval(
                9.825*d, 6*d - d*zeton, 10.425*d, 6.6*d - d*zeton,
                fill=GUI.BARVA_IGRALEC_2, tags="zeton", state="normal", width=0.03*d))

        for zeton in range(4):
            self.narisani_zetoni.append(self.plosca.create_oval(
                11.075*d, 6*d - d*zeton, 2.175*d + 9.5*d, 6.6*d - d*zeton,
                fill=GUI.BARVA_IGRALEC_2, tags="zeton", state="normal", width=0.03*d))

        self.napis.set("Na potezi je {}.".format(self.ime_1))
        self.igralec_1.igraj()

    def koncaj_igro(self, zmagovalec):
        """Konča igro in izpiše zmagovalca."""
        if zmagovalec is game_logic.IGRALEC_1:
            self.napis.set("Zmagovalec je {}. Nova igra?".format(self.ime_1))
        elif zmagovalec is game_logic.IGRALEC_2:
            self.napis.set("Zmagovalec je {}. Nova igra?".format(self.ime_2))
        elif zmagovalec is "neodloceno":
            self.napis.set("Igra je neodločena. Nova igra?".format(self.ime_2))

        self.plosca.itemconfig("zeton", state="disabled")

    def prestavi_zeton(self, zeton, polje):
        for (x, y), koordinata in self.koordinate.items():
            if koordinata == polje:
                a, b, c, d = self.plosca.coords(self.narisani_zetoni[zeton])
                self.plosca.move(self.narisani_zetoni[zeton],
                                 x - a - 0.3 * GUI.VELIKOST_ODSEKA, y - b - 0.3 * GUI.VELIKOST_ODSEKA)
                return

    def odstrani_zeton(self, zeton):
        """Nastavi tag žetonu zeton na "pojeden"."""
        self.plosca.itemconfig(self.narisani_zetoni[zeton], state="hidden", tags="pojeden")

    def klik_na_plosco(self, event):
        """Ustrezno ukrepaj ob kliku na ploščo."""
        polmer_klika = 0.3 * GUI.VELIKOST_ODSEKA

        def razdalja(x1, y1, x2, y2):
            return (x1 - x2) ** 2 + (y1 - y2) ** 2

        for id_zetona in range(18):
            a, b, c, d = self.plosca.coords(self.narisani_zetoni[id_zetona])
            if self.plosca.itemcget(self.narisani_zetoni[id_zetona], "state") == "normal" and \
               razdalja((a+c)/2, (b+d)/2, event.x, event.y) <= polmer_klika ** 2:
                if self.igra.na_potezi == game_logic.IGRALEC_1:
                    self.igralec_1.klik(id_zetona, "ZETON")
                    return
                else:
                    self.igralec_2.klik(id_zetona, "ZETON")
                    return

        for krizisce in self.koordinate:
            a, b = krizisce
            if razdalja(a, b, event.x, event.y) <= polmer_klika ** 2:
                if self.igra.na_potezi == game_logic.IGRALEC_1:
                    self.igralec_1.klik(self.koordinate[krizisce], "PLOSCA")
                    return
                else:
                    self.igralec_2.klik(self.koordinate[krizisce], "PLOSCA")
                    return

    def povleci_potezo(self, vrsta_poteze, zeton, polje=None):
        """Sprejme vrsto_poteze (PREMAKNI ali JEMLJI), zeton in po moznosti se polje (za PREMAKNI) ter odigra potezo.
        Veljavnost poteze je preverila ze metoda klik
        :param vrsta_poteze: kaksne vrste potezo naj povlece "VZEMI" ali "PREMAKNI"
        :param zeton: pri "PREMAKNI" je to id zetona, ki bo premaknjen, pri "VZEMI" pa tak, ki bo pojeden
        :param polje: pri "PREMAKNI" je to koordinata polja, kamor bo premaknjen zeton
        """

        if vrsta_poteze is "PREMAKNI":
            self.igra.odigraj_potezo(zeton, polje)
            self.prestavi_zeton(zeton, polje)
        else:
            self.igra.zakljucek_poteze(zeton)
            self.odstrani_zeton(zeton)

        # Poteza se je zakljucila - poklicali smo zakljucek_poteze ali pa se je ta poklical sam
        # (pri odigraj_potezo ni nastala trojka)
        if self.igra.konec_poteze:
            # Pogledamo ali je konec igre
            if self.igra.konec_igre:
                self.koncaj_igro(self.igra.zmagovalec)
                return
            # Ponastavimo konec_poteze
            self.igra.konec_poteze = False
            # Igralcu, ki je sedaj na potezi (igralce je ze zamenjal zakljucek_poteze) povemo, naj igra
            if self.igra.na_potezi is game_logic.IGRALEC_1:
                self.napis.set("Na potezi je {}.".format(self.ime_1))
                self.igralec_1.igraj()
            else:
                self.napis.set("Na potezi je {}.".format(self.ime_2))
                self.igralec_2.igraj()
        else:
            if self.igra.na_potezi == game_logic.IGRALEC_1:
                ime = self.ime_1
                nasprotnik = self.ime_2
            else:
                ime = self.ime_2
                nasprotnik = self.ime_1
            self.napis.set("{}, vzemi žeton igralca {}.".format(ime, nasprotnik))


class Clovek():
    """Igralec razreda Clovek"""

    def __init__(self, gui, tezavnost):
        """Objekt razreda Clovek povezemo z igralno plosco in naredimo atribute, ki bodo hranili klike"""
        self.gui = gui
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

    def igraj(self):
        """Poklice se, takoj ko pride igralec Clovek na vrsto - takrat resetiramo vse klike iz prejsnje rotacije"""
        self.prvi_klik = None
        self.drugi_klik = None
        self.tretji_klik = None

    def klik(self, koordinata, objekt):
        """Sprejme koordinato in vrsto objekta in ustrezno nadaljuje igro
        :param koordinata: ce je objekt "ZETON", potem id zetona, ce je objekt "PLOSCA", potem koordinata na plosci
        :param objekt: "ZETON" ali "PLOSCA" odvisno, kam je uporabnik kliknil
        """

        def ponastavi_barve_zetonov():
            """Ponastavi barve vseh žetonov na običajne vrednosti"""
            for krogec in self.gui.narisani_zetoni[:9]:
                self.gui.plosca.itemconfig(krogec, fill=GUI.BARVA_IGRALEC_1)
            for krogec in self.gui.narisani_zetoni[9:]:
                self.gui.plosca.itemconfig(krogec, fill=GUI.BARVA_IGRALEC_2)

        # Prvic smo kliknili na svoj zeton ali izberemo drug svoj zeton, ki ga zelimo premakniti
        # Koordinata je indeks nasega zetona (metoda klik_na_plosco ze prej preveri, da zeton ni nasprotnikov)
        if (self.prvi_klik is None or (self.drugi_klik, self.tretji_klik) == (None, None)) and objekt is "ZETON":
            self.prvi_klik = koordinata

            # Obarvanje žetona ob kliku.
            # Najprej ponastavi barve vseh žetonov, zatem preveri, če je na potezi prvi igralec in je izbran žeton
            # njegov, ter ga pobarva če je, nato enako stori za drugega igralca.
            ponastavi_barve_zetonov()
            if self.gui.igra.na_potezi == game_logic.IGRALEC_1 and koordinata < 9 and \
                    (self.gui.igra.faza_igre == 2 or self.gui.igra.zetoni[koordinata] == "zacetek"):
                self.gui.plosca.itemconfig(self.gui.narisani_zetoni[koordinata], fill=GUI.BARVA_IGRALEC_1_PRITISNJEN)
            elif self.gui.igra.na_potezi == game_logic.IGRALEC_2 and koordinata >= 9 and \
                    (self.gui.igra.faza_igre == 2 or self.gui.igra.zetoni[koordinata] == "zacetek"):
                self.gui.plosca.itemconfig(self.gui.narisani_zetoni[koordinata], fill=GUI.BARVA_IGRALEC_2_PRITISNJEN)

        # Koordinata sedaj predstavlja polje na igralni plosci
        elif (self.prvi_klik is not None and self.drugi_klik is None and objekt is "PLOSCA" and
              self.gui.igra.veljavna_poteza(self.prvi_klik, koordinata)):
            self.drugi_klik = koordinata
            self.gui.povleci_potezo("PREMAKNI", self.prvi_klik, self.drugi_klik)
            ponastavi_barve_zetonov()
        # Koordinata je indeks nasprotnikovega zetona, ki ga zelimo vzeti
        elif (self.tretji_klik is None and self.drugi_klik is not None and objekt is "ZETON" and
              self.gui.igra.veljavni_zakljucek(koordinata)):
            self.tretji_klik = koordinata
            self.gui.povleci_potezo("VZEMI", self.tretji_klik)

    def prekini(self):
        pass


class Racunalnik():
    """Igralec razreda Racunalnik"""

    def __init__(self, gui, tezavnost):
        """Objekt razreda Racunalnik povezemo z igralno plosco"""
        self.gui = gui
        self.algoritem = Alfabeta(tezavnost)
        self.mislec = None

    def igraj(self):
        """Poklice se, takoj ko pride igralec Racunalnik na vrsto"""
        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija_igre()))

        # Poženemo vlakno:
        self.mislec.start()

        # Gremo preverjat, ali je bila najdena poteza:
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            if not self.algoritem.prekinitev:
                # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
                (a, b, c) = self.algoritem.poteza
                if c is None:
                    self.gui.povleci_potezo("PREMAKNI", a, b)
                else:
                    self.gui.povleci_potezo("PREMAKNI", a, b)
                    self.gui.plosca.after(1000, lambda: self.gui.povleci_potezo("VZEMI", c))
                # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
                self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.plosca.after(100, self.preveri_potezo)


    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec:
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, koordinata, objekt):
        # Racunalnik ignorira vse klike.
        pass


class Alfabeta():
    # Algoritem alfabeta predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina):
        self.globina = globina        # do katere globine iščemo?
        self.prekinitev = False       # ali moramo končati?
        self.igra = None              # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None               # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None            # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre.
        :param igra: objekt igre, za katero racunamo naslednjo potezo, pri trenutnem stanju
        """
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False       # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None            # Sem napišemo potezo, ko jo najdemo
        # Zapomnimo si, koliko je ura
        time1 = time.time()
        # Poženemo alfabeta
        (poteza, vrednost) = self.alfabeta(self.globina, -Alfabeta.NESKONCNO, Alfabeta.NESKONCNO, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            # Počakamo, da mine vsaj ena sekunda:
            dt = time.time() - time1
            if dt < 1.0:
                time.sleep(1 - dt)
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 100000           # Mora biti vsaj 10^5
    NESKONCNO = ZMAGA + 1    # Več kot zmaga

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije"""
        vrednosti = self.igra.ocena_postavitve()
        if self.jaz is game_logic.IGRALEC_1:
            if self.igra.faza_igre == 1:
                koeficienti = (26, 1, 6, 12, 7, 1, 0)
            elif self.igra.zetoni[:9].count('izlocen') >= 6:
                koeficienti = (0, 0, 0, 10, 1, 0, 7)
            else:
                koeficienti = (43, 10, 8, 0, 0, 0, 0)
            ocena = 0
            for i in range(7):
                ocena += koeficienti[i] * vrednosti[i]
            return ocena
        else:
            if self.igra.faza_igre == 1:
                # koeficienti = (0,0,1,0,0)
                koeficienti = (26, 1, 6, 12, 7, 1, 0)
            elif self.igra.zetoni[9:].count('izlocen') >= 6:
                koeficienti = (0, 0, 0, 10, 1, 0, 7)
            else:
                koeficienti = (43, 10, 8, 0, 0, 0, 0)
            ocena = 0
            for i in range(7):
                ocena += koeficienti[i] * vrednosti[i]
            return -ocena

    def alfabeta(self, globina, alfa, beta, maksimiziramo):
        """Glavna metoda alfabeta.
        :param globina: globina algoritma alfabeta (koliko potez vnaprej pogleda)
        :param alfa: najvecja vrednost zagotovljena za maximiziranje
        :param beta: najmanja vrednost zagotovljena za minimiziranje
        :param maksimiziramo: True, ce maksimiziramo, False, ce minimiziramo
        """
        if self.prekinitev:
            return (None, None, None), 0
        if self.igra.konec_igre:
            # Igre je konec, vrnemo njeno vrednost
            if self.igra.zmagovalec == self.jaz:
                return (None, None, None), Alfabeta.ZMAGA
            elif self.igra.zmagovalec == "neodloceno":
                return (None, None, None), 0
            else:
                return (None, None, None), -Alfabeta.ZMAGA
        else:
            # Igre ni konec
            if globina == 0:
                return (None, None, None), self.vrednost_pozicije()
            else:
                # Naredimo eno stopnjo alfabeta
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = (None, None, None)
                    vrednost_najboljse = -Alfabeta.NESKONCNO
                    poteze = self.igra.veljavne_poteze()
                    random.shuffle(poteze)
                    for zeton, polje in poteze:
                        self.igra.odigraj_potezo(zeton, polje)
                        if self.igra.konec_poteze:
                            self.igra.konec_poteze = False
                            vrednost = self.alfabeta(globina - 1, alfa, beta, not maksimiziramo)[1]
                            self.igra.razveljavi()
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = (zeton, polje, None)
                            if vrednost > alfa:
                                alfa = vrednost
                            if beta <= alfa:
                                break
                        else:
                            for zeton_1 in self.igra.veljavni_zakljucki():
                                self.igra.zakljucek_poteze(zeton_1)
                                self.igra.konec_poteze = False
                                vrednost = self.alfabeta(globina - 1, alfa, beta, not maksimiziramo)[1]
                                self.igra.razveljavi()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = (zeton, polje, zeton_1)
                                if vrednost > alfa:
                                    alfa = vrednost
                                if beta <= alfa:
                                    break
                            self.igra.razveljavi()
                            if beta <= alfa:
                                break
                else:
                    # Minimiziramo
                    najboljsa_poteza = (None, None, None)
                    vrednost_najboljse = Alfabeta.NESKONCNO
                    poteze = self.igra.veljavne_poteze()
                    random.shuffle(poteze)
                    for zeton, polje in poteze:
                        self.igra.odigraj_potezo(zeton, polje)
                        if self.igra.konec_poteze:
                            self.igra.konec_poteze = False
                            vrednost = self.alfabeta(globina - 1, alfa, beta, not maksimiziramo)[1]
                            self.igra.razveljavi()
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = (zeton, polje, None)
                            if vrednost < beta:
                                beta = vrednost
                            if beta <= alfa:
                                break
                        else:
                            for zeton_1 in self.igra.veljavni_zakljucki():
                                self.igra.zakljucek_poteze(zeton_1)
                                self.igra.konec_poteze = False
                                vrednost = self.alfabeta(globina - 1, alfa, beta, not maksimiziramo)[1]
                                self.igra.razveljavi()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = (zeton, polje, zeton_1)
                                if vrednost < beta:
                                    beta = vrednost
                                if beta <= alfa:
                                    break
                            self.igra.razveljavi()
                            if beta <= alfa:
                                break

                assert (najboljsa_poteza is not (None, None, None)), "alfabeta: izračunana poteza je None"
                return najboljsa_poteza, vrednost_najboljse


if __name__ == "__main__":
    # Ustvarimo glavno okno igre
    root = tk.Tk()
    # Ime okna
    root.title("Merelles")

    # Ustvarimo objekt razreda GUI in ga pospravimo
    aplikacija = GUI(root)

    # Mainloop nadzira glavno okno in se neha izvajati ko okno zapremo
    root.mainloop()
