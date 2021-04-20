from tkinter import *

class Tablica:  
	def __init__(self,prozor,lista):
		self.prozor = prozor
		self.lista = lista
		self.len = 0
		self.tablica = []
		self.dodaj(self.lista)

	def dodaj(self, lista):
		i0 = self.len
		self.len += len(lista)
		t = [[self.dodaj_celiju(self.prozor, lista, i, j, i0) for j in range(len(lista[0]))] for i in range(len(lista))]
		self.tablica += t

	def dodaj_celiju(self, prozor, lista, i, j, i0):
		l = Label(prozor, width=10, text=lista[i][j], fg='#20bebe', font=("Cascadia Code", 18), justify='center', borderwidth=2, relief="groove")
		l.grid(row=(i+i0), column=j)
		return l

	def promijeni_vrijednost_celije(self, i, j, promijeni):
		self.tablica[i][j].config(text=promijeni)

	def promijeni_zadnji_red(self, lista):
		[ self.tablica[-1][j].config(text=lista[j]) for j in range(len(self.tablica[-1])) ]

	def vrati_vrijednost_celije(self, i, j):
		return self.tablica[i][j]["text"]