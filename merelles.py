"""Glavni del programa Merelles"""
import tkinter


class GUI():
    """Razred grafičnega vmesnika, ki izriše glavno okno komunicira med uporabnikom in igro"""

    def __init__(self, master):
        """Ustvari menije in podmenije, izriše igralno ploščo in začne igro s privzetimi nastavitvami"""

        self.master = master

        # Glavni meni
        menu = tkinter.Menu(master)
        master.config(menu=menu)

        # Podmeni Igra
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra", command=self.izbira_nove_igre)
        menu_igra.add_command(label="Izhod", command=master.destroy)

        # Podmeni Pomoč
        menu_pomoc = tkinter.Menu(menu)
        menu.add_cascade(label="Pomoč", menu=menu_pomoc)
        menu_pomoc.add_command(label="Kako igrati")  # TODO: Implementiraj okno z navodili za igro
        menu_pomoc.add_command(label="O igri")  # TODO: Implementiraj okno z informacijami o igri

        # TODO: Nariši igralno ploščo
        # TODO: Ob kliku kliči funkcijo klik
        # TODO: Začni igro s privzetimi nastavitvami

    def izbira_nove_igre(self):
        new_game = tkinter.Toplevel()
        new_game.title("Nova igra")

    def nova_igra(self, igralec_1, igralec_2, tezavnost=3):
        pass

    def koncaj_igro(self, zmagovalec=None):
        pass

    def prestavi_zeton(self, zeton, polje):
        pass

    def odstrani_zeton(self, zaton):
        pass

    def klik(self, event):
        pass

    def povleci_potezo(self, vrsta_poteze, zeton, polje=None):
        pass

if __name__ == "__main__":
    # Ustvarimo glavno okno igre
    root = tkinter.Tk()
    root.title("Merelles")

    # Ustvarimo objekt razreda GUI in ga pospravimo
    aplikacija = GUI(root)

    # Mainloop nadzira glavno okno in se neha izvajati ko okno zapremo
    root.mainloop()
