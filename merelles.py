"""Glavni del programa Merelles"""
import tkinter as tk
import game_logic


class GUI():
    """Razred grafičnega vmesnika, ki izriše glavno okno komunicira med uporabnikom in igro"""

    # Velikost delcka plosce.
    VELIKOST_ODSEKA = 100

    def __init__(self, master):
        """Ustvari menije in podmenije, izriše igralno ploščo in začne igro s privzetimi nastavitvami"""

        self.master = master
        self.igralec_1 = None
        self.igralec_2 = None
        self.igra = None
        self.ime_1 = "Rdeči"
        self.ime_2 = "Zeleni"

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
        menu_pomoc.add_command(label="Kako igrati")  # TODO: Implementiraj okno z navodili za igro
        menu_pomoc.add_command(label="O igri")  # TODO: Implementiraj okno z informacijami o igri

        # Napis igre in polje za informacije
        self.napis = tk.StringVar(self.master, value="Na potezi je {}.".format(self.ime_1))
        tk.Label(self.master, textvariable=self.napis, font=("Helvetica", 20)).grid(row=0, column=1)

        # Ustvari platno plosca in ga postavi v okno
        d = GUI.VELIKOST_ODSEKA
        self.plosca = tk.Canvas(master, width=12 * d, height=7.5 * d)
        self.plosca.grid(row=1, column=1)

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

        # Zetoni
        self.narisani_zetoni = []

        self.plosca.bind("<Button-1>", self.klik_na_plosco)
        self.new_game = None
        self.nova_igra(Clovek, Clovek)
        # TODO: Začni igro s privzetimi nastavitvami

    def izbira_nove_igre(self):
        # Ustvari novo okno za izbiro nastavitev nove igre
        if self.new_game is not None:
            self.new_game.lift()
            return
        self.new_game = tk.Toplevel()
        self.new_game.title("Merelles - Nova igra")
        self.new_game.resizable(width=False, height=False)

        self.new_game.grid_columnconfigure(0, minsize=120)
        self.new_game.grid_columnconfigure(2, minsize=150)
        self.new_game.grid_rowconfigure(0, minsize=80)
        self.new_game.grid_rowconfigure(5, minsize=70)
        self.new_game.grid_rowconfigure(9, minsize=80)

        tk.Label(self.new_game, text="Nastavitve nove igre", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=4)
        tk.Label(self.new_game, text="Izberite težavnost:").grid(row=1, column=1, sticky="W")

        tezavnosti = [("Težko", 3), ("Srednje", 2), ("Lahko", 1)]
        izbrana_tezavnost = tk.IntVar()
        izbrana_tezavnost.set(2)
        for vrstica, (besedilo, vrednost) in enumerate(tezavnosti):
            tk.Radiobutton(self.new_game, text=besedilo, variable=izbrana_tezavnost, value=vrednost, width=10,
                           anchor="w").grid(row=vrstica + 2, column=1)

        tk.Label(self.new_game, text="IGRALEC 1", font=("Helvetica", 13)).grid(row=5, column=0, sticky="E")
        tk.Label(self.new_game, text="IGRALEC 2", font=("Helvetica", 13)).grid(row=5, column=2, sticky="E")

        tk.Label(self.new_game, text="Vrsta igralca:").grid(row=6, column=0, rowspan=2, sticky="E")
        tk.Label(self.new_game, text="Vrsta igralca:").grid(row=6, column=2, rowspan=2, sticky="E")

        igralec_1_clovek = tk.BooleanVar()
        igralec_1_clovek.set(True)
        igralec_2_clovek = tk.BooleanVar()
        igralec_2_clovek.set(True)
        igralci = [("Človek", True, igralec_1_clovek, 6, 1), ("Računalnik", False, igralec_1_clovek, 7, 1),
                   ("Človek", True, igralec_2_clovek, 6, 3), ("Računalnik", False, igralec_2_clovek, 7, 3)]

        for besedilo, vrednost, spremenljivka, vrstica, stolpec in igralci:
            tk.Radiobutton(self.new_game, text=besedilo, variable=spremenljivka, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica, column=stolpec)

        tk.Label(self.new_game, text="Ime igralca:").grid(row=8, column=0, sticky="E")
        tk.Label(self.new_game, text="Ime igralca:").grid(row=8, column=2, sticky="E")

        ime_1 = tk.Entry(self.new_game, font="Helvetica 12", width=10)
        ime_1.grid(row=8, column=1)
        ime_1.insert(0, self.ime_1)
        ime_2 = tk.Entry(self.new_game, font="Helvetica 12", width=10)
        ime_2.grid(row=8, column=3)
        ime_2.insert(0, self.ime_2)

        def ustvari_igro():
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
            self.new_game.destroy()
            self.new_game = None

        def preklici():
            self.new_game.destroy()
            self.new_game = None

        tk.Button(self.new_game, text="Prekliči", width=20, height=2, command=lambda: preklici()).grid(row=9, column=0, columnspan=3, sticky="E")
        tk.Button(self.new_game, text="Začni igro", width=20, height=2, command=lambda: ustvari_igro()).grid(row=9, column=3, columnspan=3, sticky="E")

    def nova_igra(self, igralec_1, igralec_2, tezavnost=2):
        d = GUI.VELIKOST_ODSEKA

        self.igralec_1 = igralec_1(self, tezavnost)
        self.igralec_2 = igralec_2(self, tezavnost)
        self.igra = game_logic.Igra()

        self.plosca.delete("zeton")

        # Pobirisi zetone, ki so ostali na plosci

        self.narisani_zetoni = []
        for zeton in range(5):
            self.narisani_zetoni.append(self.plosca.create_oval(
                0.625*d - 0.3*d, 6.3 * d - 0.3 * d - d * zeton, 0.625 * d + 0.3 * d, 6.3 * d + 0.3 * d - d * zeton,
                fill="red", tags="zeton", state="normal"))
        for zeton in range(4):
            self.narisani_zetoni.append(self.plosca.create_oval(
                1.875 * d - 0.3 * d, 6.3 * d - 0.3 * d - d * zeton, 1.875 * d + 0.3 * d, 6.3 * d + 0.3 * d - d * zeton,
                fill="red", tags="zeton", state="normal"))

        for zeton in range(5):
            self.narisani_zetoni.append(self.plosca.create_oval(
                0.625*d - 0.3*d + 9.5 * d, 6.3 * d - 0.3 * d - d * zeton, 0.625 * d + 0.3 * d + 9.5*d,
                6.3 * d + 0.3 * d - d * zeton, fill="green", tags="zeton", state="normal"))
        for zeton in range(4):
            self.narisani_zetoni.append(self.plosca.create_oval(
                1.875 * d - 0.3 * d + 9.5 * d, 6.3 * d - 0.3 * d - d * zeton, 1.875 * d + 0.3 * d + 9.5*d,
                6.3 * d + 0.3 * d - d * zeton, fill="green", tags="zeton", state="normal"))
        self.napis.set("Na potezi je {}.".format(self.ime_1))

    def koncaj_igro(self, zmagovalec=None):
        if zmagovalec is game_logic.IGRALEC_1:
            self.napis.set("Zmagovalec je {}. Nova igra?".format(self.ime_1))
        elif zmagovalec is game_logic.IGRALEC_2:
            self.napis.set("Zmagovalec je {}. Nova igra?".format(self.ime_2))
        self.plosca.itemconfig("zeton", state="disabled")

    def prestavi_zeton(self, zeton, polje):
        for (x, y), koordinata in self.koordinate.items():
            if koordinata == polje:
                a, b, c, d = self.plosca.coords(self.narisani_zetoni[zeton])
                self.plosca.move(self.narisani_zetoni[zeton],
                                 x - a - 0.3 * GUI.VELIKOST_ODSEKA, y - b - 0.3 * GUI.VELIKOST_ODSEKA)
                return

    def odstrani_zeton(self, zeton):
        self.plosca.itemconfig(self.narisani_zetoni[zeton], state="hidden")

    def klik_na_plosco(self, event):
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
        Veljavnost poteze je preverila ze metoda klik"""
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
        """Sprejme koordinato in vrsto objekta in ustrezno nadaljuje igro"""
        # Prvic smo kliknili na svoj zeton ali izberemo drug svoj zeton, ki ga zelimo premakniti
        # Koordinata je indeks nasega zetona (metoda klik_na_plosco ze prej preveri, da zeton ni nasprotnikov)
        if (self.prvi_klik is None or (self.drugi_klik, self.tretji_klik) == (None, None)) and objekt is "ZETON":
            self.prvi_klik = koordinata
        # Koordinata sedaj predstavlja polje na igralni plosci
        elif (self.prvi_klik is not None and self.drugi_klik is None and objekt is "PLOSCA" and
              self.gui.igra.veljavna_poteza(self.prvi_klik, koordinata)):
            self.drugi_klik = koordinata
            self.gui.povleci_potezo("PREMAKNI", self.prvi_klik, self.drugi_klik)
        # Koordinata je indeks nasprotnikovega zetona, ki ga zelimo vzeti
        elif (self.tretji_klik is None and self.drugi_klik is not None and objekt is "ZETON" and
              self.gui.igra.veljavni_zakljucek(koordinata)):
            self.tretji_klik = koordinata
            self.gui.povleci_potezo("VZEMI", self.tretji_klik)


class Racunalnik():
    """Igralec razreda Racunalnik"""

    def __init__(self, gui, tezavnost):
        """Objekt razreda Racunalnik povezemo z igralno plosco"""
        self.gui = gui
        self.tezavnost = tezavnost

    def igraj(self):
        """Poklice se, takoj ko pride igralec Racunalnik na vrsto"""
        pass

    def klik(self, koordinata, objekt):
        """Racunalnik ignorira vse klike"""
        pass

                
if __name__ == "__main__":
    # Ustvarimo glavno okno igre
    root = tk.Tk()
    root.title("Merelles")

    # Ustvarimo objekt razreda GUI in ga pospravimo
    aplikacija = GUI(root)

    # Mainloop nadzira glavno okno in se neha izvajati ko okno zapremo
    root.mainloop()
