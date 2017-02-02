from __future__ import unicode_literals
from ..login.models import User
from django.db import models
import re

class AddressManager(models.Manager):
    def address_validator(self, first_name, last_name, address, city, state, zipcode, country):
        errors = []
        if len(first_name) < 2:
            errors.append("First name must be more than two characters")
        if len(last_name) < 2:
            errors.append("Last name must be more than two characters")
        if len(address) < 8:
            errors.append("Invalid address")
        if len(city) < 2 or re.search(r'[0-9]', city):
            errors.append("Invalid city")
        if len(state) < 2 or re.search(r'[0-9]', state):
            errors.append("Invalid State")
        if len(country) < 2 or re.search(r'[0-9]', country):
            errors.append("Invalid country")
        if len(zipcode) < 5 or not re.search(r'^[0-9]+$', zipcode):
            errors.append("Invalid zipcode")
        return errors



class CreditCardManager(models.Manager):
    def card_validator(self, full_name, card_number, expiration_date, cvv):
        if len(full_name) < 5 or re.search(r'[0-9]', full_name):
            errors.append("Invalid name")
        


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
