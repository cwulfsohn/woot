from __future__ import unicode_literals
from django.db import models
from ..login.models import User
import re
from datetime import datetime

class CategoryManager(models.Manager):
    def home(self):
        pass

class SubcategoryManager(models.Manager):
    def home(self):
        pass

class ProductManager(models.Manager):
    def validate(self, name, description, price, list_price, quantity, expire_date, deal_date, id=None):
        errors = []
        if len(name) < 2:
            errors.append("Name must be at least 2 characters long")
        if len(description) < 10:
            errors.append("Description must be at least 10 characters long")
        if len(price) < 2:
            errors.append("Price must be at least 2 characters long")
        p = re.compile('\d+(\.\d+)?')
        if not p.match(price):
            errors.append("Price format is digits.digits (no letters)")
        if len(list_price) < 2:
            errors.append("List price must be at least 2 characters long")
        if not p.match(list_price):
            errors.append("List price format is digits.digits (no letters)")
        if not quantity.isdigit():
            errors.append("Quantity can only be a number")
        if len(expire_date) < 6:
            errors.append("Invalid expiration date")
        else:
            expire_date = datetime.strptime(expire_date, "%m/%d/%Y")
            if expire_date < datetime.now():
                errors.append("Date must be after today")
        if deal_date:
            deal_date = datetime.strptime(deal_date, "%m/%d/%Y")
            if id:
                if Product.objects.filter(deal_date=deal_date).exclude(id=id):
                    errors.append("Already a deal on that date")
            else:
                if Product.objects.filter(deal_date=deal_date):
                    errors.append("Already a deal on that date")
        return errors

    def percent_off(self, product_price, list_price):
        percent_off = 100 * (1 - (product_price/list_price))
        return percent_off

class FeatureManager(models.Manager):
    def home(self):
        pass

class SpecificationManager(models.Manager):
    def home(self):
        pass

class SpecificationCategoryManager(models.Manager):
    def home(self):
        pass

class PurchaseManager(models.Manager):
    def home(self):
        pass

class CartManager(models.Manager):
    def home(self):
        pass

class CommentManager(models.Manager):
    def AddComment(self, comment, product_id, user_id):
        user = User.objects.get(id = user_id)
        print user.id
        product = Product.objects.get(id = product_id)
        print product.id
        Comment.objects.create(content = comment, author = user, product = product)

class LikeManager(models.Manager):
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
    name = models.CharField(max_length=255, default=None)
    primary_image = models.ImageField(null=True, upload_to="apps/home/static/home/images/", default="images/None/no-img.jpg")
    description = models.TextField()
    price = models.FloatField()
    list_price = models.FloatField(default=None)
    rating = models.FloatField(default=None)
    active = models.BooleanField(default=False)
    expire_date = models.DateTimeField()
    daily_deal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subcategory = models.ForeignKey(Subcategory, related_name="products")
    deal_date = models.DateTimeField(null=True, blank=True, default=None)
    quantity = models.IntegerField()

    objects = ProductManager()

class Image(models.Model):
    image = models.ImageField(upload_to="apps/home/static/home/images/", default="images/None/no-img.jpg")
    product = models.ForeignKey(Product, related_name="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feature(models.Model):
    header = models.CharField(max_length = 255)
    feature = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, related_name="product_features")

    objects = FeatureManager()

class SpecificationCategories(models.Model):
    category = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SpecificationCategoryManager()

class Specifications(models.Model):
    product = models.ForeignKey(Product, related_name="specifications")
    spec_category = models.ForeignKey(SpecificationCategories, related_name="products_with_spec")
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SpecificationManager()

class Cart(models.Model):
    product = models.ForeignKey(Product, related_name="products_cart")
    user = models.ForeignKey(User, related_name="users_cart")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

class Purchase(models.Model):
    user = models.ManyToManyField(User, related_name="user_purchase")
    product = models.ManyToManyField(Product, related_name="product_purchase")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PurchaseManager()

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name="user_comments")
    product = models.ForeignKey(Product, related_name="product_comments")
    reply_to = models.ForeignKey("self", null=True, default=None)

    objects = CommentManager()

class Like(models.Model):
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_likes")
    comment = models.ForeignKey(Comment, related_name="comment_likes")

    objects = LikeManager()

class Rating(models.Model):
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_rating")
    product = models.ForeignKey(Product, related_name="product_rating")
