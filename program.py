#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileWriter, PdfFileReader
import sys

zmienne = {}
aktualnaWartosc = None

for i, argument in enumerate(sys.argv):
	if i == 0:
		continue

	if argument[0] == "-":
		aktualnaWartosc = argument[1:]
		zmienne[aktualnaWartosc] = None
	else:
		zmienne[aktualnaWartosc] = argument
		aktualnaWartosc = None

if "h" in zmienne:
	print(
		u"Łączenie PDFów:",
		u"r - rozmiar (297,210)",
		u"m - margines (18,10)",
		u"ms - margines środek (10)",
		u"mo - okłatka ma posiadać margines",
		u"w - plik wyjściowy",
		"",
		sep = "\n"
	)
	exit()

if not None in zmienne:
	print("Błąd: Nie zdefiniowano pliku wejściowego")
	exit(1)

JEDNOSTKA = 72 / 25.4

plik = PdfFileReader(open(zmienne[None], "rb"))
marginesSrodek = float(zmienne["ms"]) if "ms" in zmienne else 10
okladkaBezMarginesu = "mo" in zmienne

if "r" in zmienne:
	zmienne["r"] = [float(x) for x in zmienne["r"].split(',')]

if "m" in zmienne:
	zmienne["m"] = [float(x) for x in zmienne["m"].split(',')]

rozmiar = zmienne["r"] if "r" in zmienne else (297, 210)
marginesDrukarki = zmienne["m"] if "m" in zmienne else (18, 10)

wyjscie = PdfFileWriter()

def skalujStrone(strona, wymiary):
	global JEDNOSTKA

	x = float(strona.mediaBox.getWidth()) / JEDNOSTKA
	y = float(strona.mediaBox.getHeight()) / JEDNOSTKA

	if x / y < wymiary[0] / wymiary[1]:
		strona.scaleTo((wymiary[1] / y) * x * JEDNOSTKA, wymiary[1] * JEDNOSTKA)
	else:
		strona.scaleTo(wymiary[0] * JEDNOSTKA, (wymiary[0] / x) * y * JEDNOSTKA)


def generujStrone(strona1, strona2):
	global JEDNOSTKA, wyjscie, marginesSrodek, marginesDrukarki, rozmiar, plik

	strona1 = plik.getPage(strona1) if plik.numPages > strona1 else PdfFileWriter().addBlankPage(1, 1)
	strona2 = plik.getPage(strona2) if plik.numPages > strona2 else PdfFileWriter().addBlankPage(1, 1)

	polaczonaStrona = wyjscie.addBlankPage(rozmiar[0] * JEDNOSTKA, rozmiar[1] * JEDNOSTKA)


	skalujStrone(strona1, (rozmiar[0] / 2 - marginesSrodek - marginesDrukarki[0], rozmiar[1] - marginesDrukarki[1] * 2))
	skalujStrone(strona2, (rozmiar[0] / 2 - marginesSrodek - marginesDrukarki[0], rozmiar[1] - marginesDrukarki[1] * 2))

	x1 = ((rozmiar[0] / 2 - marginesSrodek + marginesDrukarki[0]) * JEDNOSTKA - float(strona1.mediaBox.getWidth())) / 2
	x2 = ((rozmiar[0] / 2 - marginesSrodek - marginesDrukarki[0]) * JEDNOSTKA - float(strona2.mediaBox.getWidth())) / 2

	y1 = ((rozmiar[1] + marginesDrukarki[1]) * JEDNOSTKA - float(strona1.mediaBox.getHeight())) / 2
	y2 = ((rozmiar[1] + marginesDrukarki[1]) * JEDNOSTKA - float(strona2.mediaBox.getHeight())) / 2
	
	polaczonaStrona.mergeTranslatedPage(strona1, x1, y1)
	polaczonaStrona.mergeTranslatedPage(strona2, (rozmiar[0] / 2 + marginesSrodek) * JEDNOSTKA + x2, y2)


ostatnia = plik.numPages + (4 - plik.numPages % 4) % 4 - 1

print("Gererowanie okładki")

marginesTmp = marginesSrodek

if okladkaBezMarginesu:
	marginesSrodek = 0

generujStrone(ostatnia, 0)

marginesSrodek = marginesTmp

generujStrone(1, ostatnia - 1)

for i in range(1, int(plik.numPages / 4) + (1 if plik.numPages % 4 else 0)):
	print("Gererowanie stron: " + str(i * 4 - 2) + " - " + str(i * 4 + 1))
	
	generujStrone(i * 4 + 1, i * 4 - 2)
	generujStrone(i * 4 - 1, i * 4    )
	


print("Zapisywanie")

wyjscieNazwa = zmienne["w"] if "w" in zmienne else zmienne[None].split(".")

if type(wyjscieNazwa) is list:
	wyjscieNazwa[-2] += " - przekonwertowane"

	wyjscieNazwa = ".".join(wyjscieNazwa)

wyjscie.write(open(wyjscieNazwa, "wb"))
