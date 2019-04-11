"""
Napolni bazo s podatki, ki so dani v mapi podatki.

Pozeni kot

python manage.py shell -c "from miami.napolni_bazo import main; main()"
"""
from django.db import transaction
from miami.models import *
import csv
import os

def main():
	# izbrisemo vse objekte
	Igralec.objects.all().delete()
	Ekipa.objects.all().delete()
	Tekma.objects.all().delete()
	Statistika.objects.all().delete()

    IGRALCI_CSV = os.path.join(os.path.dirname(__file__), '0002_podatki', 'igralci.csv')
	EKIPE_CSV = "podatki/ekipe.csv"
	TEKME_CSV = "podatki/tekme.csv"
	STATISTIKA_CSV = "podatki/statistika.csv"

	with open(IGRALCI_CSV, encoding = 'utf-8') as f:
		for podatki in csv.DictReader(f):
			Igralec.objects.create(
				stevilka = int(podatki.pop('No.')),
				ime = podatki.pop('Player'),
				pozicija = podatki.pop('Pos'),
				visina = podatki.pop('Ht'),
				teza = int(podatki.pop('Wt')),
				letoRojstva = int(podatki.pop('Year'))
			)
			assert podatki == {}
  
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
				nasprotnik=Ekipa.objects.get(ime=podatki.pop('Opponent')),
										datum = datum,
										tockeEkipa = int(tockeEkipa),
										tockeNasportne = int(tockeNasportnik)
			)
			tekme[datum] = tekma
	#print(ekipe["Boston Celtics"].id)

	print("Shranil {} tekem".format(len(tekme)))

