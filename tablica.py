from tkinter import *

class Tablica:  
	def __init__(self, prozor, lista):
		self.prozor = prozor
		self.lista = lista
		self.len = 0
		self.tablica = []
		self.ukupno = []
		self.zbroj = []
		self.dodaj(self.lista)

	def dodaj(self, lista):
		if self.ukupno:
			self.ukupno.destroy()

		i0 = self.len
		self.len += len(lista)
		t = [ [ self.dodaj_celiju(self.prozor, lista, i, j, i0) for j in range(len(lista[0])) ] for i in range(len(lista)) ]
		self.tablica += t
		

		self.ukupno = self.dodaj_celiju(self.prozor, [["Ukupno:"]], 0, 0, self.len)
		self.ukupno.config(width=20, borderwidth=4)
		self.ukupno.grid(row=self.len, column=0, columnspan=len(self.tablica[0]))
		
		self.zbroj = [ self.dodaj_celiju(self.prozor, [[self.zbroj_stupca(i) for i in range(len(self.tablica[0]))]],
			0, j, self.len + 1) for j in range(len(self.tablica[0])) ]

	def dodaj_celiju(self, prozor, lista, i, j, i0):
		l = Label(prozor, width=10, text=lista[i][j], fg='#20bebe',
			font=("Cascadia Code", 18), justify='center', borderwidth=2, relief="groove")
		l.grid(row=(i+i0), column=j)
		return l

	def promijeni_vrijednost_celije(self, i, j, promijeni):
		self.tablica[i][j].config(text=promijeni)

	def promijeni_zadnji_red(self, lista):
		[ self.tablica[-1][j].config(text=lista[j]) for j in range(len(self.tablica[-1])) ]

		self.zbroj = [ self.dodaj_celiju(self.prozor, [[self.zbroj_stupca(i) for i in range(len(self.tablica[0]))]],
			0, j, self.len + 1) for j in range(len(self.tablica[0])) ]

	def vrati_vrijednost_celije(self, i, j):
		return self.tablica[i][j]["text"]

	def zbroj_stupca(self, i):
		return sum([int(self.tablica[j][i]["text"]) if self.tablica[j][i]["text"] != "–" else 0 for j in range(1, self.len)])