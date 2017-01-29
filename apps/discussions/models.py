from __future__ import unicode_literals
from ..login.models import User
from ..home.models import Product
from django.db import models

class CommentManager(models.Manager):
    def home(self):
        pass

class LikeManager(models.Manager):
    def home(self):
        pass

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name="user_comments")
    reply_to = models.ForeignKey(Comment, related_name="replies", default=None)
    product = models.ForeignKey(Product, related_name="product_comments")

    objects = CommentManager()

class Like(models.Model):
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="user_likes")
    comment = models.ForeignKey(Comment, related_name="comment_likes")

    objects = LikeManager()