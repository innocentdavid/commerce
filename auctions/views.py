from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    listings = Listing.objects.filter(status='open')
    listingsB = Listing.objects.filter(status='close')
    context = {'listings': listings, 'listingsB': listingsB, 'homepage': 'active'}
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
        context = {'loginpage': 'active'}
        return render(request, "auctions/login.html", context)


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
                'regpage': 'active',
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                'regpage': 'active',
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'catgspage': 'active'}
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
    context = {'watchlistpage': 'active'}
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url='/login')
def createListing(request):
    if request.POST:
        # item = Item.objects.filter(title=request.POST['title'])
        # if item:``
        #     print(item)
        #     context = {'msg': 'This item is already listed'}
        #     return HttpResponseRedirect("myListings", context)

        catg = Category.objects.get(pk=request.POST['category'])
        newItem = Item(title=request.POST['title'], description=request.POST['description'], category=catg, img_url=request.POST['imgUrl'])
        newItem.save()
        newItemId = newItem.id

        newList = Listing(author=request.user, item=Item.objects.get(pk=newItemId), current_bid=request.POST['sbid'])
        newList.save()

        return HttpResponseRedirect("myListings")

    categories = Category.objects.all()

    context = {'createlistingpage': 'active', 'categories':categories}
    return render(request, "auctions/createListing.html", context)


def bid(request):
    if request.GET:
        return HttpResponseRedirect(reverse("index"))

    if request.POST['bid']:
        bid = request.POST['bid']
        bidder = request.user
        newBid = Bid(user=bidder, item=1, bid=bid)
        newBid.save()


def myListings(request):
    listings = Listing.objects.filter(author=request.user)
    context = {'listings': listings, 'mylistingpage': 'active'}
    return render(request, "auctions/myListings.html", context)


@login_required(login_url='/login')
def listing(request):
    if request.POST:
        if request.POST['bid']:
            bid = float(request.POST['bid'])
            itemId = request.POST['itemId']

            p = Listing.objects.get(item=itemId)
            p.current_bid = bid
            p.save(update_fields=['current_bid'])

            try:
                p = Bid.objects.get(
                    item=itemId, user=User.objects.get(username=request.user))
                p.bid = bid
                p.save(update_fields=['bid'])  # or p.save() to save all
            except Bid.DoesNotExist:
                Bid.objects.create(
                    user=request.user, item=Listing.objects.get(item=itemId), bid=bid)

            context = {
                'msg': f'You Have successufully bidded this item for ${ bid } <a href="listing?q={itemId}">Go back</a>'}
            return render(request, "auctions/listing.html", context)

    id = request.GET['q']
    listings = Listing.objects.filter(item=id)

    for listing in listings:

        # for min value of bid input field
        current_bid = listing.current_bid + 1
        author = User.objects.filter(username=listing.author)

        context = {
            'listings': listings,
            'author': author,
            'current_bid': current_bid,
            'itemId': id
        }
        return render(request, "auctions/listing.html", context)


def closeL(request):
    if request.GET:
        return HttpResponseRedirect(reverse("index"))

    Lid = int(request.POST['Lid'])
    p = Listing.objects.get(item=Lid)
    p.status = 'close'
    p.save(update_fields=['status'])

    return HttpResponseRedirect(f"listing?q={Lid}")
