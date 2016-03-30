# O programu
Aplikacija Merelles je napisana v programskem jeziku Python 3 z grafičnim vmesnikom, ki uporablja knjižnico `tkinter`.

Ob zagonu aplikacije se odpre glavno okno s ploščo in igra s privzetimi nastavitvami se začne (ČLOVEK-ČLOVEK).
Če uporabnik želi igrati z računalnikom ali opazovati kako igrata dva računalnika, to lahko izbere v meniju `Igra` 
z gumbom `Nova igra`. Odpre se mu okno z nastavitvami nove igre, ki jo začne s pritiskom na gumb `Začni igro`.
Izbira lahko med tremi težavnostmi igralca računalnik, kar vpliva na število preverjenih potez vnaprej. Vsak igralec lahko
izbere tudi svoje ime.

Med igro se prikazujejo informacije v polju nad ploščo - kdo je na potezi, ali je potrebno vzeti nasprotnikov žeton, ali
je igre konec. V zadnjem primeru se izpiše ime zmagovalca, če igra ni bila neodločena. Uporabnik si lahko prebere navodila
igre v meniju `Pomoč` z izbiro `Kako igrati`.

Med igro je trenutno izbran žeton posebej označen. Če želimo izbrati drug žeton, preprosto kliknemo nanj. Če žetona ne moremo
izbrati ali premakniti na željeno polje, pomeni da to ni v skladu s pravili igre (na primer: želimo prestaviti 
nasprotnikov žeton ali premakniti žeton na polje, ki ni sosedno). 
