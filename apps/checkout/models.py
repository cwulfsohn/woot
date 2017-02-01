from __future__ import unicode_literals
from ..login.models import User
from django.db import models

class AddressManager(models.Manager):
    def home(self):
        pass

class CreditCardManager(models.Manager):
    def home(self):
        pass

class Address(models.Model):
    address = models.CharField(max_length=255)
    unit = models.CharField(max_length=40, default=None)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="user_address")

    objects = AddressManager()

class CreditCard(models.Model):
    
    objects = CreditCardManager()
# Create your models here.
