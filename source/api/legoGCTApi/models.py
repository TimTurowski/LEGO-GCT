from django.db import models


class Anbieter(models.Model):
    url = models.CharField(primary_key=True)
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Anbieter'

    def __str__(self):
        return self.name


class Einzelteil(models.Model):
    einzelteil_id = models.CharField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'Einzelteil'

    def __str__(self):
        return str(self.einzelteil_id)


class Legoset(models.Model):
    set_id = models.CharField(primary_key=True)
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Legoset'

    def __str__(self):
        return str(self.name)


class Einzelteilmarktpreis(models.Model):
    einzelteil = models.OneToOneField(Einzelteil, models.DO_NOTHING, primary_key=True)
    anbieter_url = models.ForeignKey(Anbieter, models.DO_NOTHING, db_column='anbieter_url')
    preis = models.FloatField(blank=True, null=True)
    url = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EinzelteilMarktpreis'
        unique_together = (('einzelteil', 'anbieter_url'),)

    def __str__(self):
        return str(self.einzelteil) + ' ' + str(self.anbieter_url)


class EinzelteilLegoset(models.Model):
    einzelteil = models.OneToOneField(Einzelteil, models.DO_NOTHING, primary_key=True)
    set = models.ForeignKey(Legoset, models.DO_NOTHING, db_column='set_id')
    anzahl = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Einzelteil_legoset'
        unique_together = (('einzelteil', 'set'),)

    def __str__(self):
        return str(self.einzelteil) + ' ' + str(self.set) + ' ' + str(self.anzahl)


class Setmarktpreis(models.Model):
    set = models.OneToOneField(Legoset, models.DO_NOTHING, primary_key=True)
    anbieter_url = models.ForeignKey(Anbieter, models.DO_NOTHING, db_column='anbieter_url')
    preis = models.FloatField(blank=True, null=True)
    url = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SetMarktpreis'
        unique_together = (('set', 'anbieter_url'),)

    def __str__(self):
        return str(self.anbieter_url) + ' ' + str(self.set)
