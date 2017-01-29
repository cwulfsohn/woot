from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def name_invalid(self, name):
        if not len(name) < 2 and re.search(r'^[a-zA-Z]+$', name):
            return False
        else:
            return True
    def email_invalid(self, email):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if email_regex.match(email):
            return False
        else:
            return True
    def password_invalid(self, password):
        if len(password) < 8:
            return True
        else:
            return False
    def password_not_match(self, password, confirm_password):
        if password == confirm_password:
            return False
        else:
            return True

    def reg_validator(self, username, first_name, last_name, email, password, confirm_password):
        errors = []
        if not username:
            errors.append("Username field must not be empty")
        if self.name_invalid(first_name):
            errors.append("First name must be more than two characters and only letters")
        if self.name_invalid(last_name):
            errors.append("Last name must be more than two characters and only letters")
        if self.email_invalid(email):
            errors.append("Invalid email")
        if self.password_invalid(password):
            errors.append("Password must be 8 characters or more")
        if self.password_not_match(password, confirm_password):
            errors.append("Passwords must match")
        if User.objects.filter(email=email):
            errors.append("Email already registered")
        if User.objects.filter(username=username):
            errors.append("Username already registered")
        return errors
## returns an object with either {errors: list of errors}, or {user: user object}
    def add_user(self, username, first_name, last_name, email, password, confirm_password):
        errors = self.reg_validator(username, first_name, last_name, email, password, confirm_password)
        if errors:
            return {'errors': errors}
        else:
            try:
                hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, hash_pw=hash_pw)
                user.save()
                return {"user": user}
            except:
                return {"errors": ["Something went wrong :/. Try again."]}
## returns an object with either {errors: list of errors}, or {user: user object}
    def login(self, email, password):
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode(), user.hash_pw.encode()) == user.hash_pw:
                return {"user": user}
            else:
                return {"errors": ["Invalid email or password"]}
        except:
            return {"errors": ["Invalid email or password"]}

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    hash_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
