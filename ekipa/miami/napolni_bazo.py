"""
Napolni bazo s podatki, ki so dani v mapi podatki.

Pozeni kot

python manage.py shell -c "from miami.napolni_bazo import main; main()"
"""
from django.db import transaction
from miami.models import *
import csv

def main():
#izbrisemo vse objekte
	Igralec.objects.all().delete()
	Ekipa.objects.all().delete()
	Tekma.objects.all().delete()
	Statistika.objects.all().delete()

	IGRALCI_CSV = "podatki/igralci.csv"
	EKIPE_CSV = "podatki/ekipe.csv"
	TEKME_CSV = "podatki/tekme.csv"
	STATISTIKA_CSV = "podatki/statistika.csv"

	print("Procesriam igralce...")
	igralci = {}
	with open(IGRALCI_CSV, encoding = 'utf-8') as f:
		f.readline()
		reader = csv.reader(f)

		for line in reader:
			print(line)
			stevilka, ime, pozicija, visina, teza, letoRojstva = line

			igralec = Igralec(stevilka = int(stevilka),
												ime = ime,
												pozicija = pozicija,
												visina = visina,
												teza = int(teza),
												letoRojstva =int(letoRojstva)
			)
			igralci[stevilka] = igralec
	with transaction.atomic():
		for igralec in igralci.values():
			igralec.save()
  
	print("Shranil {} igralcev".format(len(igralci)))

	print("Procesiram ekipe")
	ekipe = {}
	with open(EKIPE_CSV, encoding ='utf-8') as f:
		f.readline()
		reader = csv.reader(f)

		for line in reader:
			kratica, trener,ime = line
			ekipa = Ekipa(
										kratica = kratica,
										trener = trener,
										ime = ime
			)
			ekipe[ime] = ekipa
	
	with transaction.atomic():
		for ekipa in ekipe.values():
			ekipa.save()

	print("Shranil {} ekip".format(len(ekipe)))

	tekme = {}
	print("Procesiram tekme")
	with open(TEKME_CSV, encoding='utf-8') as f:
		f.readline()
		reader = csv.reader(f)

		for line in reader:
			datum,nasprotnik,tockeEkipa,tockeNasportnik = line
			tekma = Tekma(
										datum = datum,
										tockeEkipa = int(tockeEkipa),
										tockeNasportne = int(tockeNasportnik)
			)
			tekme[datum] = tekma
	#print(ekipe["Boston Celtics"].id)

	print("Shranil {} tekem".format(len(tekme)))

