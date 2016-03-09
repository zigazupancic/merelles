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
        self.napis = tk.StringVar(master, value="Dobrodošli v igro Merelles")
        tk.Label(master, textvariable=self.napis).grid(row=0, column=1)

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

        self.new_game = None

        self.plosca.bind("<Button-1>", self.klik_na_plosco)

        self.nova_igra(1,2,3)
        # TODO: Začni igro s privzetimi nastavitvami

    def izbira_nove_igre(self):
        # Ustvari novo okno za izbiro nastavitev nove igre
        if self.new_game is not None:
            self.new_game.focus_set()
            return
        self.new_game = tk.Toplevel()
        new_game = self.new_game
        new_game.title("Merelles - Nova igra")
        new_game.columnconfigure(3, weight=5)

        tk.Label(new_game, text="Nastavitve nove igre", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=4)
        tk.Label(new_game, text="Izberite težavnost:").grid(row=1, column=0)

        tezavnosti = [("Težko", 3), ("Srednje", 2), ("Lahko", 1)]
        izbrana_tezavnost = tk.IntVar()
        izbrana_tezavnost.set(2)
        for vrstica, (besedilo, vrednost) in enumerate(tezavnosti):
            tk.Radiobutton(new_game, text=besedilo, variable=izbrana_tezavnost, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica + 2, column=1)

        tk.Label(new_game, text="IGRALEC 1", font=("Helvetica", 13)).grid(row=5, column=0, columnspan=2)
        tk.Label(new_game, text="IGRALEC 2", font=("Helvetica", 13)).grid(row=5, column=2, columnspan=2)

        tk.Label(new_game, text="Vrsta igralca:").grid(row=6, column=0, rowspan=2)
        tk.Label(new_game, text="Vrsta igralca:").grid(row=6, column=2, rowspan=2)

        igralec_1_clovek = tk.BooleanVar()
        igralec_1_clovek.set(True)
        igralec_2_clovek = tk.BooleanVar()
        igralec_2_clovek.set(True)
        igralci = [("Človek", True, igralec_1_clovek, 6, 1), ("Računalnik", False, igralec_1_clovek, 7, 1),
                   ("Človek", True, igralec_2_clovek, 6, 3), ("Računalnik", False, igralec_2_clovek, 7, 3)]

        for besedilo, vrednost, spremenljivka, vrstica, stolpec in igralci:
            tk.Radiobutton(new_game, text=besedilo, variable=spremenljivka, value=vrednost, width=10, anchor="w")\
                .grid(row=vrstica, column=stolpec)

        tk.Label(new_game, text="Ime igralca:").grid(row=8, column=0)
        tk.Label(new_game, text="Ime igralca:").grid(row=8, column=2)

        ime_1 = tk.Entry(new_game)
        ime_1.grid(row=8, column=1)
        ime_1.insert(0, "Igralec 1")
        ime_2 = tk.Entry(new_game)
        ime_2.grid(row=8, column=3)
        ime_2.insert(0, "Igralec 2")

    def nova_igra(self, igralec_1, igralec_2, tezavnost=2):
        # Nariši žetone, pobriši žetone na plošči
        d = GUI.VELIKOST_ODSEKA

        # Pobirisi zetone, ki so ostali na plosci

        self.narisani_zetoni = []
        for zeton in range(5):
             self.narisani_zetoni.append(self.plosca.create_oval(0.625*d - 0.3*d, 6.3 * d - 0.3 * d - d * zeton, 0.625 * d + 0.3 * d, 6.3 * d + 0.3 * d - d * zeton, fill="red", tags="zeton"))
        for zeton in range(4):
             self.narisani_zetoni.append(self.plosca.create_oval(1.875 * d - 0.3 * d, 6.3 * d - 0.3 * d - d * zeton, 1.875 * d + 0.3 * d, 6.3 * d + 0.3 * d - d * zeton, fill="red", tags="zeton"))

        for zeton in range(5):
             self.narisani_zetoni.append(self.plosca.create_oval(0.625*d - 0.3*d + 9.5 * d, 6.3 * d - 0.3 * d - d * zeton, 0.625 * d + 0.3 * d + 9.5*d, 6.3 * d + 0.3 * d - d * zeton, fill="green", tags="zeton"))
        for zeton in range(4):
             self.narisani_zetoni.append(self.plosca.create_oval(1.875 * d - 0.3 * d + 9.5 * d, 6.3 * d - 0.3 * d - d * zeton, 1.875 * d + 0.3 * d + 9.5*d, 6.3 * d + 0.3 * d - d * zeton, fill="green", tags="zeton"))


    def koncaj_igro(self, zmagovalec=None):
        pass

    def prestavi_zeton(self, zeton, polje):
        for (x, y), koordinata in self.koordinate.items():
            if koordinata == polje:
                a, b, c, d = self.plosca.coords(self.narisani_zetoni[zeton])
                self.plosca.move(self.narisani_zetoni[zeton], x - a - 0.3 * GUI.VELIKOST_ODSEKA, y - b - 0.3 * GUI.VELIKOST_ODSEKA)
                return True
        return False

    def odstrani_zeton(self, zeton):
        self.plosca.delete(self.narisani_zetoni[zeton])

    def klik_na_plosco(self, event):
        polmer_klika = 0.3 * GUI.VELIKOST_ODSEKA

        def razdalja(x, y, a, b):
            return (x - a) ** 2 + (y - b) ** 2

        for id in range(18):
            a, b, c, d = self.plosca.coords(self.narisani_zetoni[id])
            if razdalja((a+c)/2, (b+d)/2, event.x, event.y) <= polmer_klika ** 2:
                if self.igra.na_potezi == game_logic.IGRALEC_1:
                    self.igralec_1.klik(id, "ZETON")
                    return
                else:
                    self.igralec_1.klik(id, "ZETON")
                    return

        for krizisce in self.koordinate:
            a, b = krizisce
            if razdalja(a, b, event.x, event.y) <= polmer_klika ** 2:
                if self.igra.na_potezi == game_logic.IGRALEC_1:
                    self.igralec_1.klik(self.koordinate[krizisce], "PLOSCA")
                    return
                else:
                    self.igralec_1.klik(self.koordinate[krizisce], "PLOSCA")
                    return

    def povleci_potezo(self, vrsta_poteze, zeton, polje=None):
        """Sprejme vrsto_poteze (PREMAKNI ali JEMLJI), zeton in po moznosti se polje (za PREMAKNI) ter odigra potezo."""
        """Veljavnost poteze je preverila ze metoda kliik"""
        if vrsta_poteze is "PREMAKNI":
            self.igra.odigraj_potezo(zeton, polje)
            self.prestavi_zeton(zeton, polje)
        else:
            self.igra.zakljucek_poteze(zeton)
            self.odstrani_zeton(zeton)
        #poteza se je zakljucila - poklicali smo zakljucek_poteze ali pa se je ta poklical sam (pri odigraj_potezo ni nastala trojka)
        if self.igra.konec_poteze:
            #pogledamo ali je konec igre
            if self.igra.konec_igre:
                self.koncaj_igro(self.igra.zmagovalec)
            #ponastavimo konec_poteze
            self.igra.konec_poteze = False
            #igralcu, ki je sedaj na potezi (igralce je ze zamenjal zakljucek_poteze) povemo, naj igra
            if self.igra.na_potezi is game_logic.IGRALEC_1:
                self.igralec_1.igraj()
            else:
                self.igralec_2.igraj()
            

class Clovek():
    """Igralec razreda Clovek"""
    
    def __init__(self, gui):
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
        #prvic smo kliknili na svoj zeton ali izberemo drug svoj zeton, ki ga zelimo premakniti
        #koordinata je indeks nasega zetona (metoda klik_na_plosco ze prej preveri, da zeton ni nasprotnikov)
        if (self.prvi_klik is None or (self.drugi_klik, self.tretji_klik) == (None, None)) and objekt is "ZETON":
            self.prvi_klik = koordinata
        #koordinata sedaj predstavlja polje na igralni plosci
        elif self.drugi_klik is None and objekt is "PLOSCA" and self.gui.igra.veljavna_poteza(self.prvi_klik, koordinata):
            self.drugi_klik = koordinata
            self.gui.povleci_potezo("PREMAKNI", self.prvi_klik, self.drugi_klik)
        #koordinata je indeks nasprotnikovega zetona, ki ga zelimo vzeti
        elif self.tretji_klik is None and self.drugi_klik is not None and objekt is "ZETON" and self.gui.igra.veljavni_zakljucek(koordinata):
            self.tretji_klik = koordinata
            self.gui.povleci_potezo("VZEMI", self.tretji_klik)



                
if __name__ == "__main__":
    # Ustvarimo glavno okno igre
    root = tk.Tk()
    root.title("Merelles")

    # Ustvarimo objekt razreda GUI in ga pospravimo
    aplikacija = GUI(root)

    # Mainloop nadzira glavno okno in se neha izvajati ko okno zapremo
    root.mainloop()
