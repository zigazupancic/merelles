"""Glavni del programa Merelles"""
import tkinter as tk


class GUI():
    """Razred grafičnega vmesnika, ki izriše glavno okno komunicira med uporabnikom in igro"""

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

        # Ustvari platno plosca in ga postavi v okno
        self.plosca = tk.Canvas(master, width=1200, height=750)
        self.plosca.grid(row=1, column=1)

        # Ozadje plošče
        self.plosca.create_rectangle(250, 10, 950, 710, fill="beige", width=0)

        # igralna plošča
        # ---------------------------------------------------------
        # Okvir
        self.plosca.create_rectangle(300, 60, 900, 660, width=6)
        self.plosca.create_rectangle(400, 160, 800, 560, width=6)
        self.plosca.create_rectangle(500, 260, 700, 460, width=6)

        self.plosca.create_line(600, 60, 600, 260, width=6)
        self.plosca.create_line(600, 460, 600, 660, width=6)
        self.plosca.create_line(300, 360, 500, 360, width=6)
        self.plosca.create_line(700, 360, 900, 360, width=6)

        # Polja
        self.plosca.create_oval(285, 45, 315, 75, fill="black")
        self.plosca.create_oval(285, 345, 315, 375, fill="black")
        self.plosca.create_oval(285, 645, 315, 675, fill="black")
        self.plosca.create_oval(885, 45, 915, 75, fill="black")
        self.plosca.create_oval(885, 345, 915, 375, fill="black")
        self.plosca.create_oval(885, 645, 915, 675, fill="black")
        self.plosca.create_oval(585, 45, 615, 75, fill="black")
        self.plosca.create_oval(585, 645, 615, 675, fill="black")

        self.plosca.create_oval(385, 145, 415, 175, fill="black")
        self.plosca.create_oval(385, 345, 415, 375, fill="black")
        self.plosca.create_oval(385, 545, 415, 575, fill="black")
        self.plosca.create_oval(785, 145, 815, 175, fill="black")
        self.plosca.create_oval(785, 345, 815, 375, fill="black")
        self.plosca.create_oval(785, 545, 815, 575, fill="black")
        self.plosca.create_oval(585, 145, 615, 175, fill="black")
        self.plosca.create_oval(585, 545, 615, 575, fill="black")

        self.plosca.create_oval(485, 245, 515, 275, fill="black")
        self.plosca.create_oval(485, 345, 515, 375, fill="black")
        self.plosca.create_oval(485, 445, 515, 475, fill="black")
        self.plosca.create_oval(685, 245, 715, 275, fill="black")
        self.plosca.create_oval(685, 345, 715, 375, fill="black")
        self.plosca.create_oval(685, 445, 715, 475, fill="black")
        self.plosca.create_oval(585, 245, 615, 275, fill="black")
        self.plosca.create_oval(585, 445, 615, 475, fill="black")
        # ---------------------------------------------------------

        # Povezava koordinat platna in koordinat polj na plosci
        self.koordinate = {(300, 60): 0, (600, 60): 1, (900, 60): 2, (400, 160): 3, (600, 160): 4, (800, 160): 5,
                           (500, 260): 6, (600, 260): 7, (700, 260): 8, (300, 360): 9, (400, 360): 10, (500, 360): 11,
                           (700, 360): 12, (800, 360): 13, (900, 360): 14, (500, 460): 15, (600, 460): 16,
                           (700, 460): 17, (400, 560): 18, (600, 560): 19, (800, 560): 20, (300, 660): 21,
                           (600, 660): 22, (900, 660): 23}

        self.plosca.bind("<Button-1>", self.klik_na_plosco)
        # TODO: Začni igro s privzetimi nastavitvami

    def izbira_nove_igre(self):
        new_game = tk.Toplevel()
        new_game.title("Nova igra")

    def nova_igra(self, igralec_1, igralec_2, tezavnost=3):
        # Nariši žetone, pobriši žetone na plošči
        # self.plosca.create_oval(35, 630, 95, 690, fill="black", tags="zeton-1")
        # self.plosca.create_oval(135, 630, 195, 690, fill="black")
        pass

    def koncaj_igro(self, zmagovalec=None):
        pass

    def prestavi_zeton(self, zeton, polje):
        pass

    def odstrani_zeton(self, zeton):
        pass

    def klik_na_plosco(self, event):
        polmer_klika = 40
        x_koordinata = round(event.x, -2)
        if event.y % 100 <= 50:
            y_koordinata = round(event.y, -2) + 60
        else:
            y_koordinata = round(event.y, -2) - 40

        if abs(x_koordinata - event.x) ** 2 + abs(y_koordinata - event.y) ** 2 <= polmer_klika ** 2:
            pass

            # TODO: poklici objekt igralca, ki je na potezi in mu povej, kaj je bilo kliknjeno

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
            if self.igra.na_potezi is IGRALEC_1:
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
