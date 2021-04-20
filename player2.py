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
			return 0
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
			return 0
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
		#print(self.ime, self.karte)

		[self.karte.remove("prazno") for i in range(self.prazne)]

		pik = [karta for karta in self.karte if '♠' in karta]
		herc = [karta for karta in self.karte if '♥' in karta]
		kara = [karta for karta in self.karte if '♦' in karta]
		tref = [karta for karta in self.karte if '♣' in karta]

		for boja in [pik, herc, kara, tref]:
			boja.sort(key=sortiraj)

		self.karte = pik + herc + kara + tref + self.prazne * ["prazno"]

		#print(self.karte)

	def odaberi_kartu(self,k,a):
		vrati = ""
		if k in self.boje():
			uber = ""
			for karta in self.karte:
				if karta[-1] == k[-1]:
					vrati = karta
					if vrijednost(karta, a) >= vrijednost(k, a):
						uber = karta
			vrati = uber if uber else vrati

			return vrati
		
		if a in self.boje():
			return [karta for karta in self.karte if karta[-1] == a][0]
			
		return [karta for karta in self.karte if karta != "prazno"][0]


	def ai_odaberi_kartu(self, adut):
		vrijednosti = list(map(lambda k: vrijednost(k, adut), [self.karte][:(8-self.prazne)]))
		return self.karte[vrijednosti.index(max(vrijednosti))]

	def baci_kartu(self, karta="", k="", a=""):
		if karta:
			#print(karta, self.karte)
			self.karte[self.karte.index(karta)] = "prazno"
			self.prazne += 1
			self.sortiraj_karte()
		elif k:
			karta = self.odaberi_kartu(k,a)

			# if k in self.boje():
			# 	karta = [karta for karta in self.karte if karta[-1] == k][0]
			# elif a in self.boje():
			# 	karta = [karta for karta in self.karte if karta[-1] == a][0]
			# else:	
			# 	karta = [karta for karta in self.karte if karta != "prazno"][0]

			self.karte[self.karte.index(karta)] = "prazno"
			self.prazne += 1
			self.sortiraj_karte()
		else:
			print("JEJ")
			karta = self.ai_odaberi_kartu(a)
			self.karte[self.karte.index(karta)] = "prazno"
			self.prazne += 1
			self.sortiraj_karte()
		return karta

	def dodaj_bodove(self, karte, adut):
		self.bodovi += sum([vrijednost(karta, adut) for karta in karte])

	def boje(self):
		boje = [karta[-1] for karta in self.karte if karta != "prazno"]
		return list(dict.fromkeys(boje))