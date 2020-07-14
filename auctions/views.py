from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    listings = Listing.objects.all()
    context = {'listings':listings}
    return render(request, "auctions/index.html", context)


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

@login_required(login_url='/login')
def listing(request):
    if not request.GET:
        return HttpResponseRedirect(reverse("index"))

    id = request.GET['q']
    listings = Listing.objects.filter(item=id)
    for listing in listings:
        # for min value of bid input field
        current_bid = listing.current_bid + 1

        author = User.objects.filter(username=listing.author)

        context = {
            'listings': listings,
            'author': author,
            'current_bid': current_bid
        }
        return render(request, "auctions/listing.html", context)

def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)

def category(request):
    if not request.GET['q']:
        return HttpResponseRedirect(reverse("index"))

    category = request.GET['q']
    listings = Item.objects.filter(category=category)
    context = {'listings': listings}
    return render(request, "auctions/category.html", context)

@login_required(login_url='/login')
def watchlist(request):
    return render(request, "auctions/watchlist.html")

@login_required(login_url='/login')
def createListing(request):
    return render(request, "auctions/createListing.html")

# def action(request):