from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 60)
    description = models.TextField()
    starting_bid = models.FloatField()
    image_url = models.URLField(blank=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watchlist = models.ManyToManyField(AuctionListing,blank=True,related_name="watchers")
    listed_items = models.ManyToManyField(AuctionListing,blank=True,related_name="creator")

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    listings = models.ManyToManyField(AuctionListing,blank=True,related_name="category")

    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bids",default="")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,related_name="bids", default='')

    def __str__(self):
        return f"{self.bid} by {self.bidder} for {self.listing.title}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(AuctionListing, on_delete = models.CASCADE, related_name="comments")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField()

    def __str__(self):
        return f"{self.message} by {self.creator}"



