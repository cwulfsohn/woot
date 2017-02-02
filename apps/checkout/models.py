from __future__ import unicode_literals
from ..login.models import User
from django.db import models

class AddressManager(models.Manager):
    pass


class CreditCardManager(models.Manager):
    def home(self):
        pass

class Address(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    unit = models.CharField(max_length=40, default=None)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="user_address", null=True, blank=True)

    objects = AddressManager()

class CreditCard(models.Model):
    last_four = models.CharField(max_length=10)
    user = models.ForeignKey(User, related_name="credit_cards", null=True, blank=True)
    full_name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, related_name="credit_cards", null=True, blank=True)
    card_number = models.CharField(max_length=255)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=255)
    objects = CreditCardManager()
# Create your models here.
