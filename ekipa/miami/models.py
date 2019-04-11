from django.db import models

# Create your models here.

class Igralec(models.Model):
    POZICIJE=(('PG', 'Playmaker'), ('SG', 'Small Guard'), 
                ('SF','Small Forward'), ('PF','Power Forward'),
                ('C','Center'))

    stevilka=models.PositiveSmallIntegerField(help_text="Številka dresa igralca")
    ime=models.CharField(max_length=200, help_text="Ime igralca")
    pozicija=models.CharField(max_length=200, choices=POZICIJE, help_text="Pozicija igralca")
    teza=models.PositiveSmallIntegerField(help_text="Teza igralca")
    visina=models.CharField(max_length = 200, help_text="Višina igralca")
    letoRojstva=models.PositiveSmallIntegerField(help_text="Leto rojstva igralca")

    class Meta:
        verbose_name_plural="Igralci"
    def __str__(self):
        return '{}:{}'.format(self.ime,self.stevilka)

class Ekipa(models.Model):
    kratica=models.CharField(max_length=200,help_text="Kratica ekipe")
    trener=models.CharField(max_length=200,help_text="Trener ekipe")
    ime=models.CharField(max_length=200,help_text="Polno ime ekipe")

    class Meta:
        verbose_name_plural="Ekipe"
    def __str__(self):
        return '{}:{}'.format(self.kratica,self.ime)

class Tekma(models.Model):
    datum=models.DateField(primary_key=True,help_text="Datum tekme", default = 2017-10-18)
    nasprotnik=models.ForeignKey('Ekipa', null=True,on_delete=models.SET_NULL, related_name="tekma_nasprotnik") 
    tockeEkipa=models.PositiveIntegerField(help_text="Točke ekipe")
    tockeNasportne=models.PositiveIntegerField(help_text="Točke nasportnika")

    def zmagala(self):
        return self.tockeEkipa > self.tockeNasportne
    
    class Meta:
        verbose_name_plural="Tekme"
    def __str__(self):
        return '{}:{}'.format(self.ekipa,self.nasprotnik)

class Statistika(models.Model):
    igralec=models.ForeignKey('Igralec', on_delete=models.CASCADE, related_name="statistika_igralec")
    tekma=models.ForeignKey('Tekma', on_delete=models.CASCADE, related_name="statistika_tekma")
    skoki=models.PositiveIntegerField(help_text="Skoki igralca")
    podaje=models.PositiveIntegerField(help_text="Podaje igralca")
    ukradene=models.PositiveIntegerField(help_text="Ukradene žoge igralca")
    tocke=models.PositiveIntegerField(help_text="Točke igralca")

    class Meta:
        verbose_name_plural="Statistike"

