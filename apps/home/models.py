from __future__ import unicode_literals
from django.db import models
from ..login.models import User

class CategoryManager(models.Manager):
    def home(self):
        pass

class SubcategoryManager(models.Manager):
    def home(self):
        pass

class ProductManager(models.Manager):
    def home(self):
        pass

class FeatureManager(models.Manager):
    def home(self):
        pass

class SpecManager(models.Manager):
    def home(self):
        pass

class PurchaseManager(models.Manager):
    def home(self):
        pass

class Category(models.Model):
    category = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CategoryManager()

class Subcategory(models.Model):
    subcategory = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name="subcategories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SubcategoryManager()

class Product(models.Model):
    description = models.TextField()
    price = models.FloatField()
    rating = models.FloatField(default=None)
    active = models.BooleanField(default=False)
    expire_date = models.DateTimeField()
    daily_deal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subcategory = models.ForeignKey(Subcategory, related_name="products")
    quantity = models.IntegerField()

    objects = ProductManager()

class Image(models.Model):
    image = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feature(models.Model):
    header = models.CharField(max_length = 255)
    feature = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ManyToManyField(Product, related_name="product_features")

    objects = FeatureManager()

class Spec(models.Model):
    header = models.CharField(max_length = 255)
    spec = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ManyToManyField(Product, related_name="product_specs")

    objects = SpecManager()

class Purchase(models.Model):
    user = models.ManyToManyField(User, related_name="user_purchase")
    product = models.ManyToManyField(Product, related_name="product_purchase")

    objects = PurchaseManager()
