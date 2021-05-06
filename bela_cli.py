from random import shuffle as promijesaj, random
from novi_player import *
from math import floor
from time import sleep

adut = []

boje = '♠ ♥ ♦ ♣'.split()

na_redu = 1

igraci = [ Igrac("Ti", False, []) ] + [ Igrac(f"AI_{i}", True, []) for i in range(1) ]

bacene_karte = [None, None]

tablica = []

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


def igrac_odgovori():
	global igraci, bacene_karte, adut

	print("Odaberi kartu:" )
	[ print(str(i+1)+str(': ')+str(igraci[0].karte[i])) for i in range(len(igraci[0].vrati_karte())) ]
	odabir = input(": ")

	odabrana_karta = igraci[0].karte[int(odabir)-1]

	if bacene_karte[1][-1] in igraci[0].boje():
		if odabrana_karta[-1] != bacene_karte[1][-1]:
			print("POGREŠNA BOJA!")
			return igrac_odgovori()
		# u_boji = [karta for karta in igraci[0].vrati_karte() if karta[-1] == bacene_karte[1][-1]]
		# uber = max(list(map(lambda k, a=adut[1][-1]: vrijednost(k,a), u_boji)))
		# bacena_vrijednost = vrijednost(bacene_karte[1], adut[1][-1])
		# print(uber, bacena_vrijednost, vrijednost(odabrana_karta, adut[1][-1]) < bacena_vrijednost)
		# if uber >= bacena_vrijednost and vrijednost(odabrana_karta, adut[1][-1]) < bacena_vrijednost:
		# 	print("BACI JACU KARTU")
		# 	return igrac_odgovori()
		return igraci[0].baci_kartu(odabrana_karta)
	elif adut[1][-1] in igraci[0].boje():
		if odabrana_karta[-1] != adut[1][-1]:
			print("BACI ADUTA!")
			return igrac_odgovori()
		else:
			return igraci[0].baci_kartu(odabrana_karta)
	else:
		return igraci[0].baci_kartu(odabrana_karta)


def vrati_pobjednika_runde():
	global adut, bacene_karte, na_redu, bacene_vrijednosti

	if bacene_karte[na_redu][-1] == adut[1][-1] and bacene_karte[int(not na_redu)][-1] != adut[1][-1]:
		return na_redu
	
	if bacene_karte[na_redu][-1] != adut[1][-1] and bacene_karte[int(not na_redu)][-1] == adut[1][-1]:
		return int(not na_redu)
	
	return bacene_vrijednosti.index(max(bacene_vrijednosti))


def napravi_potez():
	global adut, igraci, na_redu, boje, bacene_karte, bacene_vrijednosti

	print(adut, igraci[1].karte, igraci[1].prazne)
	[igrac.sortiraj_karte() for igrac in igraci]

	if na_redu == 0:
		print("Odaberi kartu:" )
		[ print(str(i+1)+str(': ')+str(igraci[0].karte[i])) for i in range(len(igraci[0].vrati_karte())) ]
		odabir = input(": ")
		if int(odabir) - 1 in range(8-igraci[0].prazne):
			bacene_karte[0] = igraci[0].baci_kartu(igraci[0].karte[int(odabir)-1])
			bacene_karte[1] = ai_baci()
	else:
		bacene_karte[1] = ai_baci()
		print(f"{igraci[1].ime} je bacio {bacene_karte[1]}")
		bacene_karte[0] = igrac_odgovori()

	## racunanje pobjednika runde

	print(bacene_karte)

	bacene_vrijednosti = list(map(lambda k, a=adut[1][-1]: vrijednost(k, a), bacene_karte))

	## funkcija vraca index pobjednika runde

	pobjednik_runde = vrati_pobjednika_runde()

	print(bacene_vrijednosti, floor(sum(bacene_vrijednosti)))

	igraci[pobjednik_runde].bodovi += floor(sum(bacene_vrijednosti))

	tablica[-1] = [igrac.bodovi for igrac in igraci]

	na_redu = pobjednik_runde

	print(sum(bacene_vrijednosti), na_redu, tablica)

	## resetrianje bacenih karti

	bacene_karte = [None, None]

	## provjera je li igra zavrsila
	if all([igrac.prazne == 8 for igrac in igraci]):
		## ako je zavrisal igrac koji je pokupio
		## zadnji stih dobiva 10 bodova
		igraci[na_redu].bodovi += 10

		## provjerava se je li igrac koji
		## je zvao pao rundu

		zvao = igraci.index(adut[0])

		if igraci[zvao].bodovi < igraci[int(not zvao)].bodovi:
			## zamjena bodova
			## '[x, y] = [x+y, 0]', tj. 'x = x + y' i 'y = 0'
			[igraci[int(not zvao)].bodovi, igraci[zvao].bodovi] = [igraci[int(not zvao)].bodovi + igraci[zvao].bodovi, 0]

		## bodovi se ponovo updejtaju
		tablica[-1] = [igrac.bodovi for igrac in igraci]
		igraci[0].ukupno += igraci[0].bodovi
		igraci[1].ukupno += igraci[1].bodovi
		if any([igrac.ukupno >= 501 for igrac in igraci]):
			igraci_bodovi = [igrac.ukupno for igrac in igraci]
			## pobjednik je igrac koji je na istom indexu
			## kao maximalni broj ukunih bodova
			pobjednik = igraci[igraci_bodovi.index(max(igraci_bodovi))]
			print(f"\n{pobjednik.ime} je pobijedio!")
			quit()
		print(tablica)
		zapocni_rundu()
	else:
		napravi_potez()


def vrati_zvanja(karte):
	global adut, boje

	ret = [0]

	if all([decko in karte for decko in 'B♠ B♥ B♦ B♣'.split()]):
		ret.append(200)

	if all([devetka in karte for devetka in '9♠ 9♥ 9♦ 9♣'.split()]):
		ret.append(150)

	if all([asevi in karte for asevi in 'A♠ A♥ A♦ A♣'.split()]):
		ret.append(100)

	if all([kraljevi in karte for kraljevi in 'K♠ K♥ K♦ K♣'.split()]):
		ret.append(100)

	if all([babe in karte for babe in 'D♠ D♥ D♦ D♣'.split()]):
		ret.append(100)

	if any([all([karta in karte for karta in f'7{boja} 8{boja} 9{boja}'.split()]) for boja in boje]):
		ret.append(20)

	return ret


def odaberi_aduta():
	global adut, igraci, na_redu, boje, gore

	print(f"Gore: {gore}")

	if na_redu == 0:
		mogucnosti = "\n1. Pik\n2. Herc\n3. Kara\n4. Tref\n5. Dalje"

		print(f"Odaberi aduta:{mogucnosti}")
		odabir = input(": ")

		if odabir in '1 2 3 4'.split():
			adut = [igraci[0], boje[int(odabir) - 1]]
		elif odabir == '5':
			adut = [igraci[1], boje[floor(random()*4)]]
		else:
			odaberi_aduta()
	else:
		ai_odabir = floor(random()*5)
		if ai_odabir == 4:
			mogucnosti = "\n1. Pik\n2. Herc\n3. Kara\n4. Tref"

			print(f"Odaberi aduta:{mogucnosti}")
			odabir = input(": ")

			if odabir in '1 2 3 4'.split():
				adut = [igraci[0], boje[int(odabir) - 1]]
			else:
				odaberi_aduta()
		else:
			adut = [igraci[1], boje[ai_odabir]]
	
	## provjeri jel ima zvanja i zamijeni sedmicu

	for igrac in igraci:
		if len(igrac.boje()) == 1:
			print(f"\n{igrac.ime} je pobijedio!")
			quit()

	if gore[-1] == adut[1][-1]:
		for igrac in igraci:
			if ('7' + adut[1][-1]) in igrac.karte:
				igrac.karte[igrac.karte.index('7' + adut[1][-1])] = gore

	zvanja = [vrati_zvanja(igrac.karte) for igrac in igraci]

	print(zvanja)

	if max(zvanja[0]) > max(zvanja[1]):
		igraci[0].bodovi += floor(sum(zvanja[0]))
	elif max(zvanja[1]) > max(zvanja[0]):
		igraci[1].bodovi += floor(sum(zvanja[1]))
	else:
		igraci[na_redu].bodovi += floor(sum(zvanja[na_redu]))


	## provjeri jel ima belu

	for igrac in igraci:
		if ('D' + adut[1][-1]) in igrac.karte and ('K' + adut[1][-1]) in igrac.karte:
			igrac.bodovi += 20

	napravi_potez()


def zapocni_rundu():
	global adut, na_redu, igraci, gore

	dek = '''
		7♠ 8♠ 9♠ 10♠ B♠ D♠ K♠ A♠
		7♥ 8♥ 9♥ 10♥ B♥ D♥ K♥ A♥
		7♦ 8♦ 9♦ 10♦ B♦ D♦ K♦ A♦
		7♣ 8♣ 9♣ 10♣ B♣ D♣ K♣ A♣
		'''.split()

	adut = []	

	na_redu = int(not na_redu)
		
	promijesaj(dek)

	for igrac in igraci:
		igrac.karte = [dek.pop() for i in range(8)]
		igrac.bodovi = 0
		igrac.prazne = 0

	gore = dek.pop()

	igraci[0].karte[0] = 'B♠'
	igraci[0].karte[1] = 'B♥'
	igraci[0].karte[2] = 'B♦'
	igraci[0].karte[3] = 'B♣'
	igraci[0].karte[4] = '7♥'
	igraci[0].karte[5] = '8♥'
	igraci[0].karte[6] = '9♥'

	[print(f"{igrac.ime}: {igrac.karte}") for igrac in igraci]

	tablica.append([0, 0])

	odaberi_aduta()


if __name__ == '__main__':
	zapocni_rundu()