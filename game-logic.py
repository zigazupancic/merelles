IGRALEC_1 = 'igralec_1'
IGRALEC_2 = 'igralec_2'

class Igra():
    def __init__(self):
        self.igralna_plosca = [None] * 24
        self.na_potezi = IGRALEC_1
        self.sosedi = [[1, 9], [0, 2, 4], [1, 14], [4, 10], [1, 3, 5, 7], [4, 13], [7, 11], [4, 6, 8], [7, 12],
                       [0, 10, 21], [3, 9, 11, 18], [6, 10, 15], [8, 13, 17], [5, 12, 14, 20], [2, 13, 23], [11, 16],
                       [15, 17, 19], [12, 16], [10, 19], [16, 18, 20, 22], [13, 19], [9, 22], [19, 21, 23], [14, 22]]
        self.trojke = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {9, 10, 11}, {12, 13, 14}, {15, 16, 17}, {18, 19, 20},
                       {21, 22, 23}, {0, 9, 21}, {3, 10, 18}, {6, 11, 15}, {1, 4, 7}, {16, 19, 22}, {8, 12, 17},
                       {5, 13, 20}, {2, 14, 23}]
        self.zetoni = [None] * 18
        self.faza_igre = 1

    def veljavna_poteza(self, zeton, zeljeno_polje):
        """Dobi index žetona, fazo igre (1-3) in index polja kamor želimo žeton postaviti"""
        if self.na_potezi is IGRALEC_1 and zeton >= 9 or self.na_potezi is IGRALEC_2 and zeton < 9:
            return False
        if self.faza_igre == 1:
            return self.igralna_plosca[zeljeno_polje] is None and self.zetoni[zeton] is None
        elif self.faza_igre == 2:
            return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in self.sosedi[self.zetoni[zeton]]
        elif self.faza_igre == 3:
            if self.na_potezi is IGRALEC_1:
                if self.zetoni[:9].count(False) >= 6:
                    return self.igralna_plosca is None
                else:
                    return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in\
                                                                          self.sosedi[self.zetoni[zeton]]
            else:
                if self.zetoni[9:].count(False) >= 6:
                    return self.igralna_plosca is None
                else:
                    return self.igralna_plosca[zeljeno_polje] is None and zeljeno_polje in\
                                                                          self.sosedi[self.zetoni[zeton]]
        else:
            return False
