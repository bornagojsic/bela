from tkinter import *
from PIL import Image, ImageTk

primarna_boja = "#20bebe"
font = ("Cascadia Code", 18)
bold_font = ("Cascadia Code", 18, "bold")
naslovni_font = ("Cascadia Code", 32, "bold")


def vrati_igru_label(prozor, text):
	global font, primarna_boja
	return Label(prozor, text=text, font=font, fg=primarna_boja, pady=15)


def vrati_naslov(prozor, text):
	global naslovni_font, primarna_boja
	return Label(prozor, text=text, font=naslovni_font, fg=primarna_boja)


def vrati_gumb(prozor, text, command):
	global font, primarna_boja
	return Button(prozor, text=text, font=font, bg=primarna_boja, fg="#fff",
		activebackground='#eee', activeforeground='#10aeae', command=command)#, relief="flat")


def vrati_entry(prozor, sirina=10):
	global font, primarna_boja
	return Entry(prozor, width=sirina, font=font, fg=primarna_boja)


def svi_podwidgeti(prozor):
	widgeti = prozor.winfo_children()

	for widget in widgeti:
		if widget.winfo_children():
			widgeti.extend(widget.winfo_children())

	return widgeti


def izbrisi(widget):
	try:
		if widget.winfo_class() != "Toplevel":
			widget.destroy()
	except:
		pass


def ocisti_prozor(prozor):
	## počinje se brisati od indexa 2 jer su nulti i prvi element
	## canvas i pozadina koje ne želimo obrisati pri čišćenju prozora
	[ izbrisi(widget) for widget in svi_podwidgeti(prozor)[2:]  ]
	# for widget in svi_podwidgeti(prozor)[2:]:
	# 	if widget.winfo_class() != "Toplevel":
	# 		try:
	# 			widget.destroy()
	# 		except:
	# 			pass


def vrati_sliku(prozor, path, sirina=0, visina=0):
	slika = Image.open(path)
	if sirina and visina:
		slika = slika.resize((sirina, visina), Image.ANTIALIAS)
	slika = ImageTk.PhotoImage(slika)
	return slika


def vrati_sliku_label(prozor, path, sirina=0, visina=0):
	slika = vrati_sliku(prozor, path, sirina, visina)
	slika_label = Label(image=slika)
	slika_label.image = slika
	return slika_label


def vrati_sliku_gumb(prozor, path, sirina=0, visina=0, command=lambda: None):
	global font, primarna_boja
	slika = vrati_sliku(prozor, path, sirina, visina)
	gumb = Button(prozor, image=slika, font=font, bg=primarna_boja, fg="#fff",
		activebackground='#eee', activeforeground='#10aeae', command=command)
	gumb.image = slika
	return gumb