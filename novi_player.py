def sortiraj(karta):
	karta = karta[:-1]
	if karta in "7 8 9 10".split():
		return int(karta)-10
	elif karta == "B":
		return 2
	elif karta == "D":
		return 3
	elif karta == "K":
		return 4
	elif karta == "A":
		return 11

def vrijednost(karta, adut):
	if karta[-1] == adut:
		karta = karta[:-1]
		if karta in ["7", "8"]:
			return int(karta) / 100
		elif karta == "9":
			return 14
		elif karta == "10":
			return 10
		elif karta == "B":
			return 20
		elif karta == "D":
			return 3
		elif karta == "K":
			return 4
		elif karta == "A":
			return 11
	else:
		karta = karta[:-1]
		if karta in "7 8 9".split():
			return int(karta) / 100
		elif karta == "10":
			return 10
		elif karta == "B":
			return 2
		elif karta == "D":
			return 3
		elif karta == "K":
			return 4
		elif karta == "A":
			return 11


class Igrac():
	def __init__(self, ime, ai, karte):
		self.ime = ime
		self.ai = ai
		self.karte = karte
		self.prazne = 0
		self.bodovi = 0
		self.ukupno = 0
	
	def sortiraj_karte(self):
		[self.karte.remove("prazno") for i in range(self.prazne)]

		pik = [karta for karta in self.karte if '♠' in karta]
		herc = [karta for karta in self.karte if '♥' in karta]
		kara = [karta for karta in self.karte if '♦' in karta]
		tref = [karta for karta in self.karte if '♣' in karta]

		for boja in [pik, herc, kara, tref]:
			boja.sort(key=sortiraj)

		self.karte = pik + herc + kara + tref + self.prazne * ["prazno"]

	def baci_kartu(self, karta):
		print(self.ime, self.prazne, self.karte)
		self.karte[self.karte.index(karta)] = "prazno"
		self.prazne += 1
		self.sortiraj_karte()
		print(self.ime, self.prazne, self.karte)
		return karta

	def boje(self):
		boje = [karta[-1] for karta in self.karte if karta != "prazno"]
		return list(dict.fromkeys(boje))

	def vrati_karte(self):
		return self.karte[:8-self.prazne]