from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=90)
    location = models.CharField(max_length=200)
    link = models.CharField(max_length=250,null=True)
    category = models.CharField(max_length=200,null=True)
    price = models.CharField(max_length=30)
    def __str__(self):
        return self.title
        return self.date
        return self.location
        return self.link
        return self.category
        return self.price

class Preferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=1000, null=True)
    rating = models.CharField(max_length=2, null=True)
class Interested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=90)
    location = models.CharField(max_length=200)
    link = models.CharField(max_length=250,null=True)
    category = models.CharField(max_length=200,null=True)
    price = models.CharField(max_length=30)
    def __str__(self):
        return self.title
        return self.date
        return self.location
        return self.link
        return self.category
        return self.price
