import sys
import json
from dek import *
from tablica import *
from math import floor
from novi_player import *
from moj_tkinter import *
from datetime import datetime
from tkinter import messagebox
from os import listdir, mkdir, remove
from random import shuffle as promijesaj, random


sirina = 9 * 25 // 4
visina = 9 * 40 // 4

y0 = 5
sirina_prozora = 712
visina_prozora = 950

sirina_slike = 2590//10
visina_slike = 2130//10

vrati_bela_slika = lambda prozor: vrati_sliku_label(prozor, "karte/bela-removebg.png", sirina_slike, visina_slike)

dek = '''
		7♠ 8♠ 9♠ 10♠ B♠ D♠ K♠ A♠
		7♥ 8♥ 9♥ 10♥ B♥ D♥ K♥ A♥
		7♦ 8♦ 9♦ 10♦ B♦ D♦ K♦ A♦
		7♣ 8♣ 9♣ 10♣ B♣ D♣ K♣ A♣
		'''.split()

boje = '♠ ♥ ♦ ♣'.split()

adut = []

igrac_na_redu = 0

tablica = ""
tablica_prozor = ""

bacene_karte = ["prazno", "prazno"]

bacene_karte_labeli = []

def funkcija(prozor, adut):
	global igraci, igrac_na_redu

	pokazi_karte(prozor)

	bacene_karte = ["prazno", "prazno"]

	if igrac_na_redu == 1:
		print("HEJ")

		karta = igraci[1].baci_kartu(a=adut)

		karta_label = vrati_sliku_label(prozor, f"karte/{karta}.png", 9*sirina//10, 9*visina//10)

		karta_label.grid(row=3, column=3)


def vrati_kartu_gumb(prozor, path, sirina, visina, karta):
	gumb = vrati_sliku_gumb(prozor, path, sirina, visina, lambda k=karta: odigraj_kartu(k))
	gumb.config(borderwidth=0, bg="#666")
	return gumb


def nova_runda(prozor):
	global tablica, broj_igraca, adut_gumbi, dalje, gornja_karta, adut, igrac_na_redu, dek, meni

	ocisti_igru(prozor)

	print("NOVA RUNDA")

	dek = '''
		7♠ 8♠ 9♠ 10♠ B♠ D♠ K♠ A♠
		7♥ 8♥ 9♥ 10♥ B♥ D♥ K♥ A♥
		7♦ 8♦ 9♦ 10♦ B♦ D♦ K♦ A♦
		7♣ 8♣ 9♣ 10♣ B♣ D♣ K♣ A♣
		'''.split()

	adut = []

	meni = vrati_gumb(prozor, "☰", pokazi_meni)
	
	meni.grid(row=0, column=0)

	# bela(prozor, 2)

	if broj_igraca == 2:
		global adut_gumbi, dalje

		tablica.dodaj([[0, 0]])
		
		promijesaj(dek)

		for igrac in igraci:
			igrac.karte = [dek.pop() for i in range(8)]
			igrac.prazne = 0

		gornja_karta = dek.pop()

		adut_gumbi = [ vrati_sliku_gumb(prozor, f"karte/{boje[i]}.png", 50, 50, lambda p=prozor, j=i: odaberi_aduta(p, boje[j])) for i in range(4) ]
		
		dalje = vrati_gumb(prozor, "Dalje", lambda p=prozor: odaberi_aduta(p))

		igrac_na_redu = int(not igrac_na_redu)

		[adut_gumbi[i].grid(column=(i if i < 2 else i+1), columnspan=2, row=7) for i in range(4)]
		dalje.grid(column=2, columnspan=2, row=7)
		
		## ako je 1 onda je true
		if igrac_na_redu:
			if random() >= 0.5:
				dalje.config(bg="#bebebe", state="disabled")
			else:
				odaberi_aduta(prozor)

		postavi_igru(prozor)


def ai_baci():
	global igraci, bacene_karte, adut

	if bacene_karte[0]:
		if bacene_karte[0][-1] in igraci[1].boje():
			moguce = [karta for karta in igraci[1].karte if karta[-1] == bacene_karte[0][-1]]
			moguce_vrijednosti = list(map(lambda k, a=adut[1][-1]: vrijednost(k, a), moguce))
			return igraci[1].baci_kartu(moguce[moguce_vrijednosti.index(max(moguce_vrijednosti))])
		elif adut[1][-1] in igraci[1].boje():
			moguce = [karta for karta in igraci[1].karte if karta[-1] == adut[1][-1]]
			moguce_vrijednosti = list(map(lambda k, a=adut[1][-1]: vrijednost(k, a), moguce))
			return igraci[1].baci_kartu(moguce[moguce_vrijednosti.index(max(moguce_vrijednosti))])
		
		return igraci[1].baci_kartu(igraci[1].karte[floor(random() * (8-igraci[1].prazne))]) 
	
	return igraci[1].baci_kartu(igraci[1].karte[floor(random() * (8-igraci[1].prazne))])


def odigraj_kartu(odabrana_karta):
	global igraci
	
	## true je ako je igrac na redu 1
	if igrac_na_redu:
		igrac_odgovori(odabrana_karta)
		if bacene_karte[0]:
			igrac_je_odigrao.set(1)
	else:
		bacene_karte[0] = igraci[0].baci_kartu(odabrana_karta)
		igrac_je_odigrao.set(1)


def igrac_odgovori(odabrana_karta):
	global igraci, bacene_karte, adut

	print(odabrana_karta)

	if bacene_karte[1][-1] in igraci[0].boje():
		if odabrana_karta[-1] != bacene_karte[1][-1]:
			messagebox.showwarning("Upozorenje", "Pogrešna boja!")
			return
		# u_boji = [karta for karta in igraci[0].vrati_karte() if karta[-1] == bacene_karte[1][-1]]
		# uber = max(list(map(lambda k, a=adut[1][-1]: vrijednost(k,a), u_boji)))
		# bacena_vrijednost = vrijednost(bacene_karte[1], adut[1][-1])
		# print(uber, bacena_vrijednost, vrijednost(odabrana_karta, adut[1][-1]) < bacena_vrijednost)
		# if uber >= bacena_vrijednost and vrijednost(odabrana_karta, adut[1][-1]) < bacena_vrijednost:
		# 	print("BACI JACU KARTU")
		# 	return igrac_odgovori()
		igrac_je_odigrao.set(1)
		bacene_karte[0] = igraci[0].baci_kartu(odabrana_karta)
		print(f"{bacene_karte} su bacene")
		return
	if adut[1][-1] in igraci[0].boje():
		if odabrana_karta[-1] != adut[1][-1]:
			messagebox.showwarning("Upozorenje", "Baci aduta!")
			return
		igrac_je_odigrao.set(1)
		bacene_karte[0] = igraci[0].baci_kartu(odabrana_karta)
		print(f"{bacene_karte} su bacene")
		return
	igrac_je_odigrao.set(1)
	bacene_karte[0] = igraci[0].baci_kartu(odabrana_karta)
	print(f"{bacene_karte} su bacene")
	return


def vrati_pobjednika_runde():
	global adut, bacene_karte, igrac_na_redu, bacene_vrijednosti

	if bacene_karte[igrac_na_redu][-1] == adut[1][-1] and bacene_karte[int(not igrac_na_redu)][-1] != adut[1][-1]:
		return igrac_na_redu
	
	if bacene_karte[igrac_na_redu][-1] != adut[1][-1] and bacene_karte[int(not igrac_na_redu)][-1] == adut[1][-1]:
		return int(not igrac_na_redu)
	
	return bacene_vrijednosti.index(max(bacene_vrijednosti))


def ocisti_igru(prozor):
	widgeti = svi_podwidgeti(prozor)[2:]

	widgeti = list(filter(lambda w: w.winfo_class() != "Toplevel", widgeti))

	widgeti = [w for w in widgeti if w.grid_info()]

	widgeti = list(filter(lambda w: w.grid_info()["in"].winfo_class() != "Toplevel", widgeti))

	[widget.destroy() for widget in widgeti]


def pokazi_karte(prozor):
	global adut, igraci, bacene_karte, bacene_vrijednosti, igrac_na_redu

	ocisti_igru(prozor)

	meni = vrati_gumb(prozor, "☰", pokazi_meni)
	
	meni.grid(row=0, column=0)

	adut_label = Label(prozor, text=f"Adut:", font=(bold_font), fg=primarna_boja)

	adut_boja_label = vrati_sliku_label(prozor, f"karte/{adut[1]}.png", 50, 50)
	
	adut_label.grid(column=2, row=7)
	adut_boja_label.grid(column=3, row=7)

	prikazi_igru(prozor)

	print(bacene_karte)

	bacene_karte_labeli = [ vrati_sliku_label(prozor, f"karte/{karta if karta else 'prazno'}.png", 9*sirina//10, 9*visina//10)
								for karta in bacene_karte ]

	[igrac.sortiraj_karte() for igrac in igraci] ## malo je redundant kad se bacaju karte

	polje1 = vrati_sliku_label(prozor, f"karte/prazno.png", sirina, visina)
	polje2 = vrati_sliku_label(prozor, f"karte/prazno.png", sirina, visina)
	polje1.grid(row=3, column=2)
	polje2.grid(row=3, column=3)
	
	for i in range(5,7):
		for j in range(1,5):
			karta = igraci[0].karte[(i-5)*4+j-1]
			karta = vrati_kartu_gumb(prozor, f"karte/{karta}.png", 9*sirina//10, 9*visina//10, karta)
			karta.grid(column=j, row=i)

	for i in range(1,3):
		for j in range(1,5):
			if igraci[1].karte[(i-1)*4+j-1] == "prazno":
				karta = vrati_sliku_label(prozor, f"karte/prazno.png", 9*sirina//10, 9*visina//10)
			else:
				karta = vrati_sliku_label(prozor, f"karte/prekrenuta.png", 9*sirina//10, 9*visina//10)
			karta.grid(column=j, row=i)

	if igrac_na_redu == 0:
		prozor.wait_variable(igrac_je_odigrao)
		bacene_karte[1] = ai_baci()
	else:
		bacene_karte[1] = ai_baci()
		bacene_karte_labeli[1] = vrati_sliku_label(prozor, f"karte/{bacene_karte[1]}.png", 9*sirina//10, 9*visina//10)
		bacene_karte_labeli[1].grid(row=3, column=3)
		print(f"{igraci[1].ime} je bacio {bacene_karte}")
		prozor.wait_variable(igrac_je_odigrao)
		#bacene_karte[0] = igrac_odgovori()

	print(bacene_karte, adut)

	igrac_je_odigrao.set(0)

	bacene_vrijednosti = list(map(lambda k, a=adut[1][-1]: vrijednost(k, a), bacene_karte))

	## funkcija vraca index pobjednika runde

	pobjednik_runde = vrati_pobjednika_runde()

	print(bacene_vrijednosti, floor(sum(bacene_vrijednosti)))

	igraci[pobjednik_runde].bodovi += floor(sum(bacene_vrijednosti))

	tablica.promijeni_zadnji_red([igrac.bodovi for igrac in igraci])

	igrac_na_redu = pobjednik_runde

	print(sum(bacene_vrijednosti), igrac_na_redu, tablica)

	## resetrianje bacenih karti

	bacene_karte = [None, None]

	## provjera je li igra zavrsila
	if all([igrac.prazne == 8 for igrac in igraci]):
		## ako je zavrisal igrac koji je pokupio
		## zadnji stih dobiva 10 bodova
		igraci[igrac_na_redu].bodovi += 10

		## provjerava se je li igrac koji
		## je zvao pao rundu

		zvao = igraci.index(adut[0])

		if igraci[zvao].bodovi < igraci[int(not zvao)].bodovi:
			## zamjena bodova
			## '[x, y] = [x+y, 0]', tj. 'x = x + y' i 'y = 0'
			[igraci[int(not zvao)].bodovi, igraci[zvao].bodovi] = [igraci[int(not zvao)].bodovi + igraci[zvao].bodovi, 0]

		## bodovi se ponovo updejtaju
		tablica.promijeni_zadnji_red([igrac.bodovi if igrac.bodovi else "–" for igrac in igraci])
		igraci[0].ukupno += igraci[0].bodovi
		igraci[1].ukupno += igraci[1].bodovi
		if any([igrac.ukupno >= 101 for igrac in igraci]):
			igraci_bodovi = [igrac.ukupno for igrac in igraci]
			## pobjednik je igrac koji je na istom indexu
			## kao maximalni broj ukunih bodova
			pobjednik = igraci[igraci_bodovi.index(max(igraci_bodovi))]
			messagebox.showinfo("Gotovo", f"\n{pobjednik.ime} je pobijedio!")
			pocetna(prozor)
		print(tablica.tablica)
		adut_je_odabran.set(0)
		nova_runda(prozor)

	bacene_karte_labeli[0].grid(row=3, column=2)
	bacene_karte_labeli[1].destroy()

	#pokazi_karte(prozor)

	postavi_igru(prozor)


def prikazi_karte(prozor):
	for i in range(5,7):
		for j in range(1,4):
			karta = igraci[0].karte[(i-6)*4+j]
			karta = vrati_sliku_label(prozor, f"karte/{karta}.png", 9*sirina//10, 9*visina//10)
			karta.grid(column=j, row=i)
		karta = vrati_sliku_label(prozor, f"karte/prekrenuta.png", 9*sirina//10, 9*visina//10)
		karta.grid(column=4, row=i)

	for i in range(1,3):
		for j in range(1,5):
			karta = vrati_sliku_label(prozor, f"karte/prekrenuta.png", 9*sirina//10, 9*visina//10)
			karta.grid(column=j, row=i)


def prikazi_igru(prozor):
	global sirina, visina, gornja_karta, adut, tablica, tablica_prozor, sirina_prozora, y0, adut_je_odabran

	podloga2 = vrati_sliku_label(prozor, "karte/podloga.png", 9*sirina, 28*visina//10)
	podloga1 = vrati_sliku_label(prozor, "karte/podloga.png", 9*sirina, 28*visina//10)
	gornja_karta_label = vrati_sliku_label(prozor, f"karte/{gornja_karta}.png", 9*sirina//10, 9*visina//10)
	ime1_label = Label(text=igraci[0].ime, font=bold_font, fg=primarna_boja)
	ime2_label = Label(text=igraci[1].ime, font=bold_font, fg=primarna_boja)
	polje1 = vrati_sliku_label(prozor, f"karte/prazno.png", sirina, visina)
	polje2 = vrati_sliku_label(prozor, f"karte/prazno.png", sirina, visina)

	podloga1.grid(row=1, column=1, columnspan=4, rowspan=2)
	podloga2.grid(row=5, column=1, columnspan=4, rowspan=2)
	gornja_karta_label.grid(column=0, row=3, columnspan=2)
	ime1_label.grid(column=2, row=8, columnspan=2)
	ime2_label.grid(column=2, row=0, columnspan=2)
	polje1.grid(row=3,column=2)
	polje2.grid(row=3,column=3)

	if not tablica_prozor:
		tablica_prozor = Toplevel(prozor)
		tablica_prozor.geometry(f"+{sirina_prozora+5}+{y0}")
		tablica_prozor.title("Bela")
		tablica_prozor.iconbitmap('karte/tref.ico')
		tablica_prozor.resizable(False, False)
		tablica_prozor.protocol("WM_DELETE_WINDOW", lambda: None)

		tablica = Tablica(tablica_prozor, [[ igrac.ime for igrac in igraci ], [0, 0]])


def postavi_igru(prozor):
	prikazi_igru(prozor)

	prikazi_karte(prozor)
	print("ADUT:", adut, adut_je_odabran.get())
	if not adut:
		prozor.wait_variable(adut_je_odabran)
	pokazi_karte(prozor)


def odaberi_aduta(prozor, odabrani_adut=""):
	global adut, adut_label, adut_gumbi, dalje

	[adut_gumb.destroy() for adut_gumb in adut_gumbi]
	dalje.destroy()

	adut = [igraci[0], odabrani_adut] if odabrani_adut else [igraci[1], boje[floor(random()*4)]]

	adut_label = Label(prozor, text=f"Adut:", font=(bold_font), fg=primarna_boja)

	adut_boja_label = vrati_sliku_label(prozor, f"karte/{adut[1]}.png", 50, 50)
	
	adut_label.grid(column=2, row=7)
	adut_boja_label.grid(column=3, row=7)
	
	adut_je_odabran.set(1)

	postavi_igru(prozor)


def nastavi_igru():
	meni_label.destroy()
	bela_slika.destroy()
	nastavi_igru_gumb.destroy()
	spremi_igru_gumb.destroy()
	vrati_se_na_pocetnu_gumb.destroy()
	izadi_bez_spremanja_gumb.destroy()

	spremljeno = False

	[ w.grid(row=c["row"], column=c["column"], rowspan=c["rowspan"], columnspan=c["columnspan"]) for ([w, c]) in widgeti ]


def spremi_ime_igre(prozor, izadi_nakon_spremanja, vrati_se_na_pocetnu, pocetni_prozor):
	global spremljene_igre, adut, broj_igraca, tablica_prozor

	ime_igre = ime_igre_unos.get()

	if ime_igre:
		if str(ime_igre) in spremljene_igre:
			messagebox.showerror('Pogreška', 'Već postoji spremljena igra s ovim imenom!')
			ime_igre_unos.delete(0, END)
			prozor.lift()
		elif any([ znak in str(ime_igre) for znak in '/ \\ : ? * \" \' < > |'.split() ]):
			messagebox.showerror('Pogreška', 'Ime ne smije sadržavati znakove / \\ : ? * \" \' < > |!')
			ime_igre_unos.delete(0, END)
			prozor.lift()
		elif len(str(ime_igre)) > 20:
			messagebox.showerror('Pogreška', 'Ime mora sadržavati manje od 20 znakova!')
			ime_igre_unos.delete(0, END)
			prozor.lift()
		else:
			time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")

			if adut:
				adut = [adut[0], igraci.index(adut[1])]

			with open(f'spremljene igre/{ime_igre}.igra', 'w', encoding='utf8') as file:
				json.dump([time] + [[ igrac.__dict__ for igrac in igraci ]] + [gornja_karta] + [adut] + [broj_igraca],
					file, ensure_ascii=False)

			spremljene_igre.append(ime_igre)

			global spremljeno

			spremljeno = True

			prozor.destroy()
			sys.exit()
	else:
		messagebox.showerror('Pogreška', 'Molimo upišite ime za spremanje igre!')
		prozor.lift()

	if izadi_nakon_spremanja:
		prozor.destory()
	elif vrati_se_na_pocetnu:
		tablica_prozor.destroy()
		tablica_prozor = ""
		pocetna(pocetni_prozor)


def spremi_igru(prozor, izadi=False, pocetna=False):
	global ime_igre_unos

	spremanje_prozor = Toplevel(prozor)
	spremanje_prozor.title("Spremanje")
	spremanje_prozor.iconbitmap('karte/tref.ico')
	spremanje_prozor.resizable(False, False)

	spremanje_canvas = Canvas(spremanje_prozor, width=300, height=250)
	spremanje_canvas.grid(rowspan=3, columnspan=1)

	ime_igre_label = Label(spremanje_prozor, text="Unesi ime igre:", font=bold_font, fg=primarna_boja)
	ime_igre_unos = vrati_entry(spremanje_prozor, 20)

	spremi_ime_igre_gumb = vrati_gumb(spremanje_prozor, "Spremi igru",
		lambda: spremi_ime_igre(spremanje_prozor, izadi, pocetna, prozor))

	ime_igre_label.grid(row=0, column=0)
	ime_igre_unos.grid(row=1, column=0)
	spremi_ime_igre_gumb.grid(row=2, column=0)


def vrati_se_na_pocetnu(prozor):
	global tablica_prozor
	if spremljeno:
		tablica_prozor.destroy()
		tablica_prozor = ""
		pocetna(prozor)

	if messagebox.askyesno("Izađi", "Želite li se vratiti na početni meni bez spremanja?"):
		tablica_prozor.destroy()
		tablica_prozor = ""
		pocetna(prozor)
	else:
		spremi_igru(prozor, pocetna=True)


def izadi_bez_spremanja(prozor):
	if spremljeno:
		prozor.destroy()
		sys.exit()

	if messagebox.askyesno("Izađi", "Želite li izaći bez spremanja?"):
		prozor.destroy()
		sys.exit()
	else:
		spremi_igru(prozor, izadi=True)


def pokazi_meni():
	global meni_label, bela_slika, nastavi_igru_gumb, spremi_igru_gumb, vrati_se_na_pocetnu_gumb, izadi_bez_spremanja_gumb
	global widgeti, spremljeno
	
	spremljeno = False

	widgeti = svi_podwidgeti(prozor)[2:]

	widgeti = list(filter(lambda w: w.winfo_class() != "Toplevel", widgeti))

	widgeti = [w for w in widgeti if w.grid_info()]

	widgeti = list(filter(lambda w: w.grid_info()["in"].winfo_class() != "Toplevel", widgeti))

	widgeti = [ [widget, widget.grid_info()] for widget in widgeti ]
	
	[ widget[0].grid_forget() for widget in widgeti ]
	
	meni_label = vrati_naslov(prozor, "Meni")
	
	bela_slika = vrati_bela_slika(prozor)

	nastavi_igru_gumb = vrati_gumb(prozor, "Nastavi", lambda: nastavi_igru())
	spremi_igru_gumb = vrati_gumb(prozor, "Spremi", lambda: spremi_igru(prozor))
	vrati_se_na_pocetnu_gumb = vrati_gumb(prozor, "Početni meni", lambda: vrati_se_na_pocetnu(prozor))
	izadi_bez_spremanja_gumb = vrati_gumb(prozor, "Izađi", lambda: izadi_bez_spremanja(prozor))

	#spremi_igru_gumb.config(bg="#bebebe", state="disabled")

	meni_label.grid(row=0, column=2, columnspan=2)
	bela_slika.grid(row=1, column=1, columnspan=4, rowspan=3)
	nastavi_igru_gumb.grid(row=4, column=2, columnspan=2)
	spremi_igru_gumb.grid(row=5, column=2, columnspan=2)
	vrati_se_na_pocetnu_gumb.grid(row=6, column=2, columnspan=2)
	izadi_bez_spremanja_gumb.grid(row=7, column=2, columnspan=2)


def bela(prozor, broj_i):
	global igraci, gornja_karta, broj_igraca, dek

	broj_igraca = broj_i

	ocisti_prozor(prozor)

	igraci = [ Igrac("Ti", False, []) ] + [ Igrac(f"AI_{i}", True, []) for i in range(broj_igraca-1) ]
	
	promijesaj(dek)

	meni = vrati_gumb(prozor, "☰", pokazi_meni)
	
	meni.grid(row=0, column=0)

	if broj_igraca == 2:
		global adut_gumbi, dalje

		canvas.grid(rowspan=9, columnspan=6)
		pozadina.grid(rowspan=9, columnspan=6)

		for igrac in igraci:
			igrac.karte = [dek.pop() for i in range(8)]
			igrac.prazne = 0

		gornja_karta = dek.pop()

		adut_gumbi = [ vrati_sliku_gumb(prozor, f"karte/{boje[i]}.png", 50, 50, lambda p=prozor, j=i: odaberi_aduta(p, boje[j])) for i in range(4) ]
		
		dalje = vrati_gumb(prozor, "Dalje", lambda p=prozor: odaberi_aduta(p))
		
		[adut_gumbi[i].grid(column=(i if i < 2 else i+1), columnspan=2, row=7) for i in range(4)]
		dalje.grid(column=2, columnspan=2, row=7)

		postavi_igru(prozor)



def nova_igra(prozor):
	ocisti_prozor(prozor)

	bela_title = vrati_naslov(prozor, "Nova igra")

	bela_slika = vrati_bela_slika(prozor)

	nova_igra_gumb = vrati_gumb(prozor, text="Započni novu igru", command=nova_igra)

	bele = [ vrati_gumb(prozor, text=f"Bela u {i}", command=lambda p=prozor, broj=i: bela(p, broj)) for i in [2,3,4] ] 
	
	povratak = vrati_gumb(prozor, text="Povratak", command=lambda p=prozor: pocetna(p))

	[ bele[i-2].config(bg="#bebebe", state="disabled") for i in [3,4] ]

	bela_title.grid(column=1, row=0)
	bela_slika.grid(column=1,row=1)
	[ bele[i-2].grid(column=1, row=i) for i in [2,3,4] ]
	povratak.grid(column=1, row=5)


def ucitaj_spremljenu_igru(igra):
	global igraci, gornja_karta, adut, broj_igraca, adut_je_odabran

	with open(f'spremljene igre/{igra}.igra', 'r', encoding='utf8') as file:
		[vrijeme, igraci_, gornja_karta_, adut_, broj_igraca_] = json.load(file)

	igraci_lista = [ Igrac(igrac["ime"], igrac["ai"], igrac["karte"]) for igrac in igraci_]

	for i in range(broj_igraca_):
		igraci_lista[i].prazne = igraci_[i]["prazne"]
		igraci_lista[i].bodovi = igraci_[i]["bodovi"]
		igraci_lista[i].ukupno = igraci_[i]["ukupno"]

	igraci = igraci_lista
	gornja_karta = gornja_karta_
	adut = adut_
	broj_igraca = broj_igraca_

	print(f"{igraci=}, {gornja_karta=}, {adut=}, {broj_igraca=}")
	
	ocisti_prozor(prozor)

	meni = vrati_gumb(prozor, "☰", pokazi_meni)
	
	meni.grid(row=0, column=0)

	if broj_igraca == 2:
		canvas.grid(rowspan=9, columnspan=6)
		pozadina.grid(rowspan=9, columnspan=6)

	if adut:
		adut_je_odabran.set(1)

		adut = [igraci[adut[1]], adut[0]]

		adut_label = Label(prozor, text=f"Adut:", font=(bold_font), fg=primarna_boja)

		adut_boja_label = vrati_sliku_label(prozor, f"karte/{adut[0]}.png", 50, 50)
		
		adut_label.grid(column=2, row=7)
		adut_boja_label.grid(column=3, row=7)
	else:
		global adut_gumbi, dalje

		adut_gumbi = [ vrati_sliku_gumb(prozor, f"karte/{boje[i]}.png", 50, 50, lambda p=prozor, j=i: odaberi_aduta(p, boje[j])) for i in range(4) ]
		
		dalje = vrati_gumb(prozor, "Dalje", lambda p=prozor: odaberi_aduta(p))
		
		[adut_gumbi[i].grid(column=(i if i < 2 else i+1), columnspan=2, row=7) for i in range(4)]
		dalje.grid(column=2, columnspan=2, row=7)

	postavi_igru(prozor)


def izbrisi_spremljenu_igru(prozor, igra):
	global spremljene_igre

	remove(f"spremljene igre/{spremljene_igre[igra]}.igra")

	del spremljene_igre[igra]

	nastavi_spremljenu_igru(prozor, spremljene_igre)


def nastavi_spremljenu_igru(prozor, spremljene_igre):
	ocisti_prozor(prozor)

	nastavi_igru_label = vrati_naslov(prozor, "Nastavi igru")

	print(spremljene_igre)

	container = Frame(prozor)
	canvas = Canvas(container)
	scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
	igre_frame = Frame(canvas)

	igre_frame.bind(
		"<Configure>",
		lambda e: canvas.configure(
			scrollregion=canvas.bbox("all")
	    )
	)

	canvas.create_window((0, 0), window=igre_frame,  anchor="nw")

	canvas.configure(yscrollcommand=scrollbar.set)

	for i in range(len(spremljene_igre)):
		igra_gumb = vrati_gumb(igre_frame, spremljene_igre[i], lambda j=i: ucitaj_spremljenu_igru(spremljene_igre[j]))
		igra_gumb.config(width=20)

		igra_izbrisi_gumb = vrati_gumb(igre_frame, "🗑", lambda j=i: izbrisi_spremljenu_igru(prozor, j))
		
		igra_gumb.grid(row=i, column=0, pady=10, padx=10)
		igra_izbrisi_gumb.grid(row=i, column=1, pady=10, padx=10)

	container.grid(column=1, row=1, rowspan=3)
	canvas.grid(row=0, column=1, rowspan=3)
	scrollbar.grid(row=0, column=2, sticky='ns', rowspan=3)

	povratak = vrati_gumb(prozor, "Povratak", lambda p=prozor: pocetna(p))

	nastavi_igru_label.grid(column=1, row=0)
	povratak.grid(column=1, row=5)


def o_beli(prozor):
	global primarna_boja, canvas
	ocisti_prozor(prozor)

	bela_title = vrati_naslov(prozor, "O beli")

	bela_slika = vrati_bela_slika(prozor)

	t1 = "Ova je igra nastala kao projekt Borne Gojšića iz nastvnog predmeta Informatika u 3. razredu prirodoslovo-matematičke"
	t2 = "gimnazije pohađane u Gimnaziji Karlovac, pod mentorstvom prof. Igora Petrovića u šk. god. 2020/2021."
	t3 = "Zabranjeno je svako kopiranje, redistribuiranje i plagiranje izvornog koda ove igre i/ili intelektualnog vlasništva autora bez kontaktiranja autora!"

	t = [t1+t2,t3]

	poruke = [ Message(prozor, text=t[i], font=font, fg=primarna_boja, width=650, justify='center') for i in [0,1] ]

	povratak = vrati_gumb(prozor, text="Povratak", command=lambda p=prozor: pocetna(p))
	
	bela_title.grid(column=1, row=0)
	bela_slika.grid(column=1,row=1)
	poruke[0].grid(column=0, row=2, columnspan=3, rowspan=2)
	poruke[1].grid(column=0, row=4, columnspan=3)
	povratak.grid(column=1, row=5)


def pocetna(prozor):
	global spremljene_igre, adut

	adut = []

	ocisti_prozor(prozor)

	canvas.grid(columnspan=3,rowspan=6)	

	bela_title = vrati_naslov(prozor, "Bela")

	bela_slika = vrati_bela_slika(prozor)

	nova_igra_gumb = vrati_gumb(prozor, text="Započni novu igru", command=lambda p=prozor: nova_igra(p))

	try:
		spremljene_igre = list(map(lambda ime: ime[:-5], listdir("spremljene igre/")))
	except:
		mkdir("spremljene igre")
		spremljene_igre = []
	nastavi_spremljenu_igru_gumb = vrati_gumb(prozor, text="Nastavi prošlu igru",
		command=lambda p=prozor, s=spremljene_igre: nastavi_spremljenu_igru(p, s))
	if not spremljene_igre:
		nastavi_spremljenu_igru_gumb.config(bg="#bebebe", state="disabled")
	
	o_beli_gumb = vrati_gumb(prozor, text="O igri", command=lambda p=prozor: o_beli(p)) 
	
	izadi = vrati_gumb(prozor, text="Izađi", command=quit)

	bela_title.grid(column=1, row=0)
	bela_slika.grid(column=1,row=1)
	nova_igra_gumb.grid(column=1, row=2)
	nastavi_spremljenu_igru_gumb.grid(column=1, row=3)
	o_beli_gumb.grid(column=1, row=4)
	izadi.grid(column=1, row=5)


prozor = Tk()
prozor.geometry(f"+0+{y0}")
prozor.title("Bela")
prozor.iconbitmap('karte/tref.ico')
prozor.resizable(False, False)

canvas = Canvas(prozor, width=sirina_prozora, height=visina_prozora)
canvas.grid(columnspan=3,rowspan=6)

pozadina = vrati_sliku_label(prozor, "karte/pozadina.png")

pozadina.grid(row=0,column=0,rowspan=6,columnspan=3)

igrac_je_odigrao = IntVar()

adut_je_odabran = IntVar()

pocetna(prozor)

prozor.mainloop()