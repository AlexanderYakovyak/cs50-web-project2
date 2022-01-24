from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

from .models import *

class AuctionListingForm(ModelForm):
    category = forms.CharField(max_length=64,required = False)
    class Meta: 
        model = AuctionListing
        fields = ["title","description","starting_bid","image_url"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["message",]

def index(request):
    return render(request, "auctions/index.html",{
            "listings":AuctionListing.objects.filter(closed=False),
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def check_watchlist(request,listing_id):
    in_watchlist = False

    if request.user.is_authenticated:
        try:
            request.user.watchlist.get(id=listing_id)
            in_watchlist = True
        except ObjectDoesNotExist: 
            pass

    return in_watchlist

def auction_listing(request,listing_id):

    in_watchlist = check_watchlist(request,listing_id)

    if request.method == "POST":
        if request.POST.get("to_watchlist") == "add":
            request.user.watchlist.add(AuctionListing.objects.get(id=listing_id))
        elif request.POST.get("to_watchlist") == "remove":
            request.user.watchlist.remove(AuctionListing.objects.get(id=listing_id))
        elif request.POST.get("bid") is not None:
            current_listing = AuctionListing.objects.get(id=listing_id)

            if float(request.POST.get("bid"))>current_listing.bids.last().bid:
                Bid.objects.filter(listing=current_listing).delete()
                bid = Bid(bid=float(request.POST.get("bid")),bidder = request.user,listing=current_listing)
                bid.save()
            else:
                return render(request,"auctions/listing.html",{
                    "listing": AuctionListing.objects.get(pk=listing_id),
                    "comment": CommentForm(),
                    "in_watchlist": in_watchlist,
                    "message": "Your bid should be greated than a current bid. Please, place another one."
                })
        elif request.POST.get("end_listing") is not None:
            current_listing = AuctionListing.objects.get(id=listing_id)
            current_listing.closed = True
            current_listing.save()
        else:
            form = CommentForm(request.POST)
            if form.is_valid():

                new_comment = Comment(listing = AuctionListing.objects.get(id=listing_id),
                                      creator = request.user,message=form.cleaned_data['message'])
                new_comment.save()

        return HttpResponseRedirect(reverse('auction_listing',args=[listing_id]))
    else:
        return render(request,"auctions/listing.html",{
            "listing": AuctionListing.objects.get(pk=listing_id),
            "comment": CommentForm(),
            "in_watchlist": in_watchlist,
        })

def new_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():

            if not form.cleaned_data['image_url']:
                img = "https://mizez.com/custom/mizez/img/general/no-image-available.png"
            else:
                img = form.cleaned_data['image_url']

            listing_new = AuctionListing(title=form.cleaned_data['title'],
                                     description=form.cleaned_data['description'],
                                     starting_bid =float(form.cleaned_data['starting_bid']),
                                     image_url = img)
 
            listing_new.save()
            listing_new.creator.add(request.user)
            listing_new.save()
               
            if float(form.cleaned_data['starting_bid'])>=0:
                bid = Bid(bid = float(form.cleaned_data['starting_bid']), bidder = request.user,listing = listing_new)
                bid.save()
            else:
                AuctionListing.objects.get(id = listing_new.id).delete()
                return render(request,'auctions/new_listing.html',{
                    "form":form,
                    "message": "Starting bid can't be less than zero!",
                })

            category = form.cleaned_data['category'].title()

            try: 
                category = Category.objects.get(name=category)
                category.listings.add(listing_new)
            except ObjectDoesNotExist:
                if category!='':
                    new_category = Category(name=category)
                    new_category.save()
                    new_category.listings.add(listing_new)

            return HttpResponseRedirect(reverse('auction_listing',args=[listing_new.id]))
        else:
            return render(request, "auctions/new_listing.html", {
                    "form":form
                })

    else:
        return render(request,"auctions/new_listing.html",{
                "form": AuctionListingForm(),
            })

def categories(request):
    return render(request,"auctions/categories.html",{
            "categories": Category.objects.all(),
        })

def category(request,category_name):
    category_listings = Category.objects.get(name=category_name).listings.filter(closed=False)
    return render(request,"auctions/category.html", {
            "category_listings":category_listings,
            "category":category_name,
        })

def watchlist(request):
    return render(request,"auctions/watchlist.html", {
            "watchlist_listings": request.user.watchlist.all(),
        })

def won_auctions(request):
    won_listings = AuctionListing.objects.filter(closed=True, bids__bidder = request.user)
    return render(request,"auctions/won.html",{
            "won_listings":won_listings,
        })

def listed_auctions(request):
    listed_items = AuctionListing.objects.filter(creator = request.user)
    return render(request,"auctions/listed.html",{
            "listed_items":listed_items,
        })