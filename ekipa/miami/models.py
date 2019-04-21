from django.db import models


class Igralec(models.Model):
    PLAYMAKER, SMALL_GUARD, SMALL_FORWARD, POWER_FORWARD, CENTER = 'PG', 'SG', 'SF', 'PF', 'C'
    POZICIJE = (
        (PLAYMAKER, 'Playmaker'),
        (SMALL_GUARD, 'Small Guard'),
        (SMALL_FORWARD, 'Small Forward'),
        (POWER_FORWARD, 'Power Forward'),
        (CENTER, 'Center'),
    )

    stevilka = models.PositiveSmallIntegerField(help_text="Številka dresa igralca")
    ime = models.CharField(max_length=200, help_text="Ime igralca")
    pozicija = models.CharField(max_length=200, choices=POZICIJE, help_text="Pozicija igralca")
    teza = models.PositiveSmallIntegerField(help_text="Teža igralca")
    visina = models.CharField(max_length=200, help_text="Višina igralca")
    leto_rojstva = models.PositiveSmallIntegerField(help_text="Leto rojstva igralca")
    slika = models.ImageField(upload_to="igralci/", default="igralci/missing.jpg")

    class Meta:
        verbose_name_plural = 'igralci'

    def __str__(self):
        return '{}:{}'.format(self.ime, self.stevilka)


class Ekipa(models.Model):
    kratica = models.CharField(max_length=200, help_text="Kratica ekipe", unique=True)
    trener = models.CharField(max_length=200, help_text="Trener ekipe")
    ime = models.CharField(max_length=200, help_text="Polno ime ekipe", unique=True)

    class Meta:
        verbose_name_plural = "Ekipe"

    def __str__(self):
        return '{}: {}'.format(self.kratica, self.ime)



class Tekma(models.Model):
    datum = models.DateField(help_text="Datum tekme", default=2017-10-18)
    nasprotnik = models.ForeignKey('Ekipa', null=True, on_delete=models.SET_NULL, related_name="tekma_nasprotnik")
    tocke_ekipa = models.PositiveIntegerField(help_text="Točke ekipe")
    tocke_nasprotne = models.PositiveIntegerField(help_text="Točke nasportnika")

    def zmagala(self):
        return self.tocke_ekipa > self.tocke_nasprotne

    class Meta:
        verbose_name_plural = "Tekme"
        unique_together = ('datum', 'nasprotnik')

    def __str__(self):
        return '{}: {}'.format(self.datum, self.nasprotnik)


class Statistika(models.Model):
    igralec = models.ForeignKey(
        'Igralec', on_delete=models.CASCADE, related_name="statistika_igralec")
    tekma = models.ForeignKey(
        'Tekma', on_delete=models.CASCADE, related_name="statistika_tekma")
    skoki = models.PositiveIntegerField(help_text="Skoki igralca")
    podaje = models.PositiveIntegerField(help_text="Podaje igralca")
    ukradene = models.PositiveIntegerField(help_text="Ukradene žoge igralca")
    tocke = models.PositiveIntegerField(help_text="Točke igralca")

    class Meta:
        verbose_name_plural = "Statistike"
