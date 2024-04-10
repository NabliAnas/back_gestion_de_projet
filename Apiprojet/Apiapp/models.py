from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
class Role(models.Model):
    role_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(AbstractUser):
    username = models.CharField(max_length=150)
    firstname = models.CharField(max_length=150, blank=True, null=True)
    lastname = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal = models.CharField(max_length=20, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    id_role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1) 
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    def __str__(self):
        return self.username
class Type(models.Model):
    type_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Client(models.Model):
    raison_sociale = models.CharField(max_length=255)
    responsable = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Projet(models.Model):
    id_projet = models.BigAutoField(primary_key=True)
    date_creation = models.DateField(auto_now_add=True)
    designiation = models.CharField(max_length=255)
    description = models.TextField()
    Annee = models.PositiveSmallIntegerField(default=date.today().year)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    mode_facturation = models.CharField(max_length=255)
    Duree = models.IntegerField(null=True)
    id_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    ancien_taux_realisation = models.FloatField(default=0)
    new_taux_realisation = models.FloatField(default=0)
    montant_ht = models.FloatField()
    nbrJh = models.IntegerField(null=True)
    tarif = models.FloatField(null=True)
    statut = models.BooleanField(default=False)
    facturation = models.BooleanField(default=False)
    recouvrement = models.BooleanField(default=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Archive(models.Model):
    ancien_taux_realisation = models.FloatField()
    new_taux_realisation = models.FloatField()
    id_projet = models.ForeignKey('Projet', on_delete=models.CASCADE)
    commentaire = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Facture(models.Model):
    id_projet = models.ForeignKey('Projet', on_delete=models.CASCADE)
    prix_unitaire = models.FloatField(null=True)
    quantite = models.FloatField(null=True)
    taux_tva = models.FloatField(default=0.2)
    total_tva = models.FloatField()
    total_ht = models.FloatField()
    total_ttc = models.FloatField()
    unite = models.CharField(max_length=50)
    reference = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
