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

        # Ustvari platno in ga postavi v okno
        self.platno = tk.Canvas(master, width=1200, height=750)
        self.platno.grid(row=1, column=1)

        # Ozadje plošče
        self.platno.create_rectangle(250, 10, 950, 710, fill="beige", width=0)

        # igralna plošča
        # ---------------------------------------------------------
        # Okvir
        self.platno.create_rectangle(300, 60, 900, 660, width=6)
        self.platno.create_rectangle(400, 160, 800, 560, width=6)
        self.platno.create_rectangle(500, 260, 700, 460, width=6)

        self.platno.create_line(600, 60, 600, 260, width=6)
        self.platno.create_line(600, 460, 600, 660, width=6)
        self.platno.create_line(300, 360, 500, 360, width=6)
        self.platno.create_line(700, 360, 900, 360, width=6)

        # Polja
        self.platno.create_oval(285, 45, 315, 75, fill="black")
        self.platno.create_oval(285, 345, 315, 375, fill="black")
        self.platno.create_oval(285, 645, 315, 675, fill="black")
        self.platno.create_oval(885, 45, 915, 75, fill="black")
        self.platno.create_oval(885, 345, 915, 375, fill="black")
        self.platno.create_oval(885, 645, 915, 675, fill="black")
        self.platno.create_oval(585, 45, 615, 75, fill="black")
        self.platno.create_oval(585, 645, 615, 675, fill="black")

        self.platno.create_oval(385, 145, 415, 175, fill="black")
        self.platno.create_oval(385, 345, 415, 375, fill="black")
        self.platno.create_oval(385, 545, 415, 575, fill="black")
        self.platno.create_oval(785, 145, 815, 175, fill="black")
        self.platno.create_oval(785, 345, 815, 375, fill="black")
        self.platno.create_oval(785, 545, 815, 575, fill="black")
        self.platno.create_oval(585, 145, 615, 175, fill="black")
        self.platno.create_oval(585, 545, 615, 575, fill="black")

        self.platno.create_oval(485, 245, 515, 275, fill="black")
        self.platno.create_oval(485, 345, 515, 375, fill="black")
        self.platno.create_oval(485, 445, 515, 475, fill="black")
        self.platno.create_oval(685, 245, 715, 275, fill="black")
        self.platno.create_oval(685, 345, 715, 375, fill="black")
        self.platno.create_oval(685, 445, 715, 475, fill="black")
        self.platno.create_oval(585, 245, 615, 275, fill="black")
        self.platno.create_oval(585, 445, 615, 475, fill="black")
        # ---------------------------------------------------------


        # TODO: Ob kliku kliči funkcijo klik
        # TODO: Začni igro s privzetimi nastavitvami

    def izbira_nove_igre(self):
        new_game = tk.Toplevel()
        new_game.title("Nova igra")

    def nova_igra(self, igralec_1, igralec_2, tezavnost=3):
        pass

    def koncaj_igro(self, zmagovalec=None):
        pass

    def prestavi_zeton(self, zeton, polje):
        pass

    def odstrani_zeton(self, zeton):
        pass

    def klik(self, event):  # TODO: spremeni ime, da ne pride do zmešnjave z razredom človek in računalnik
        pass

    def povleci_potezo(self, vrsta_poteze, zeton, polje=None):
        pass

if __name__ == "__main__":
    # Ustvarimo glavno okno igre
    root = tk.Tk()
    root.title("Merelles")

    # Ustvarimo objekt razreda GUI in ga pospravimo
    aplikacija = GUI(root)

    # Mainloop nadzira glavno okno in se neha izvajati ko okno zapremo
    root.mainloop()
