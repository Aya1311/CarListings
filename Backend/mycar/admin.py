# mycar/admin.py
from django.contrib import admin
from .models import CarMoteur, CarAvito, Admin, Client, ConcreteCar, Sauvegarde, Visite

# Enregistrement des modèles pour l'administration Django
admin.site.register(CarMoteur)
admin.site.register(CarAvito)
admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(ConcreteCar)
admin.site.register(Sauvegarde)
admin.site.register(Visite)


