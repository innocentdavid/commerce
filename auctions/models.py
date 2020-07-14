from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.category

class Item(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    img_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item  = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    
    def __str__(self):
        return str(self.item)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    bid = models.FloatField(default=0, null=False, blank=False)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.item)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(null=True, blank=False)
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)

