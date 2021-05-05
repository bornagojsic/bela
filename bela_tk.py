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
	## funkcija koja handle-a to da ai baci kartu koju treba
	global igraci, bacene_karte, adut

	if bacene_karte[0]:
		if bacene_karte[0][-1] in igraci[1].boje():
			for karta in igraci[1].karte:
				if karta[-1] == bacene_karte[0][-1]:
					return igraci[1].baci_kartu(karta)
		elif adut[1][-1] in igraci[1].boje():
			for karta in igraci[1].karte:
				if karta[-1] == adut[1][-1]:
					return igraci[1].baci_kartu(karta)
		
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
		else:
			return igraci[0].baci_kartu(odabrana_karta)
	elif adut[1][-1] in igraci[0].boje():
		if odabrana_karta[-1] != adut[1][-1]:
			print("BACI ADUTA!")
			return igrac_odgovori()
		else:
			return igraci[0].baci_kartu(odabrana_karta)
	else:
		return igraci[0].baci_kartu(odabrana_karta)


def napravi_potez():
	global adut, igraci, na_redu, boje, bacene_karte

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

	print(bacene_karte)

	bacene_vrijednosti = list(map(lambda k, a=adut[1][-1]: vrijednost(k, a), bacene_karte))

	print(bacene_vrijednosti)

	pobjednik_runde = bacene_vrijednosti.index(max(bacene_vrijednosti))

	igraci[pobjednik_runde].bodovi += sum(bacene_vrijednosti)

	tablica[-1] = [igrac.bodovi for igrac in igraci]

	na_redu = pobjednik_runde

	print(sum(bacene_vrijednosti), na_redu, tablica)

	bacene_karte = [None, None]

	if all([igrac.prazne == 8 for igrac in igraci]):
		igraci[na_redu].bodovi += 10
		tablica[-1] = [igrac.bodovi for igrac in igraci]
		igraci[0].ukupno += igraci[0].bodovi
		igraci[1].ukupno += igraci[1].bodovi
		if any([igrac.ukupno >= 101 for igrac in igraci]):
			igraci_bodovi = [igrac.ukupno for igrac in igraci]
			pobjednik = igraci[igraci_bodovi.index(max(igraci_bodovi))]
			print(f"\n{pobjednik.ime} je pobijedio!")
			quit()
		print(tablica)
		zapocni_rundu()
	else:
		napravi_potez()


def odaberi_aduta():
	global adut, igraci, na_redu, boje

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
		napravi_potez()
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
		napravi_potez()


def zapocni_rundu():
	global adut, na_redu, igraci

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

	[print(f"{igrac.ime}: {igrac.karte}") for igrac in igraci]

	tablica.append([0, 0])

	odaberi_aduta()


if __name__ == '__main__':
	zapocni_rundu()