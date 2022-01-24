from django.contrib import admin

from .models import *
# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid", "bidder", "listing")

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid,BidAdmin)
admin.site.register(AuctionListing,AuctionListingAdmin)
admin.site.register(Comment)