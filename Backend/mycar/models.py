from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='admin')

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return self.user.username

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    carburant_prefere = models.CharField(max_length=100, null=True, blank=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    boite_preferee = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.user.username

class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    carburant = models.CharField(max_length=50, null=True, blank=True)
    boite = models.CharField(max_length=50, null=True, blank=True)
    puissance_fiscale = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=500)
    kilometrage = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=255, null=True, blank=True)
    scraped_at = models.DateTimeField(default=now)
    nombre_de_portes = models.CharField(max_length=50, null=True, blank=True, default="N/A")
    autor = models.CharField(max_length=255, null=True, default="N/A")
    etat = models.CharField(max_length=50, null=True, blank=True, default="N/A")

    class Meta:
        abstract = True

class CarAvito(Car):
    def __str__(self):
        return self.title

class CarMoteur(Car):
    def __str__(self):
        return self.title

class ConcreteCar(Car):
    class Meta:
        verbose_name = 'Concrete Car'
        verbose_name_plural = 'Concrete Cars'

class Sauvegarde(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(CarAvito, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'car')
        verbose_name = 'Client-Car Sauvegarde'
        verbose_name_plural = 'Client-Cars Sauvegardes'

class Visite(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(CarAvito, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'car')
        verbose_name = 'Client-Car Visite'
        verbose_name_plural = 'Client-Cars Visites'

