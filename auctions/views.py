from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    listings = Listing.objects.filter(status='open')
    context = {'listings': listings, 'homepage': 'active'}
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

    catg = request.GET['q']
    category = Category.objects.get(pk=catg)

    listings = Item.objects.filter(category=catg)
    context = {'listings': listings, 'category': category}
    return render(request, "auctions/category.html", context)


@login_required(login_url='/login')
def watchlist(request):
    if request.POST:
        id = request.POST['Lid']
        Watchlist.objects.filter(user=request.user, item=Item.objects.get(pk=id)).delete()

        return HttpResponseRedirect(reverse("watchlist"))

    watchlist = Watchlist.objects.filter(user=request.user)
    items = [Item.objects.get(title=item) for item in watchlist]
    listings = [Listing.objects.get(item__title=items) for items in items]
    
    context = {'watchlistpage': 'active', 'listings': listings}
    return render(request, "auctions/watchlist.html", context)

@login_required(login_url='/login')
def createListing(request):
    if request.POST:

        # item = Item.objects.filter(title=request.POST['title'])
        # if item:
        #     print(item)
        #     context = {'msg': 'This item is already listed'}
        #     return HttpResponseRedirect("myListings", context)

        catg = Category.objects.get(pk=request.POST['category'])
        newItem = Item(title=request.POST['title'], description=request.POST['description'],
                       category=catg, img_url=request.POST['imgUrl'])
        newItem.save()
        newItemId = newItem.id

        newList = Listing(author=request.user, item=Item.objects.get(
            pk=newItemId), current_bid=request.POST['sbid'])
        newList.save()

        return HttpResponseRedirect("myListings")

    categories = Category.objects.all()

    context = {'createlistingpage': 'active', 'categories': categories}
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
    listings = Listing.objects.filter(author=request.user).order_by('-status')
    context = {'listings': listings, 'mylistingpage': 'active'}
    return render(request, "auctions/myListings.html", context)


@login_required(login_url='/login')
def listing(request):
    if request.POST:
        # place a bid
        try:
            bid = request.POST['bid']
            itemId = request.POST['itemId']

            p = Listing.objects.get(item=itemId)
            p.current_bid = bid
            p.save(update_fields=['current_bid'])

            # add to watchlist automatically on first bid
            watchlist = Watchlist.objects.filter(user=request.user, item=itemId)
            if not watchlist:
                add = Watchlist(user=request.user, item=Item.objects.get(pk=itemId))
                add.save()
                
            try:
                p = Bid.objects.get(
                    item=itemId, user=User.objects.get(username=request.user))
                p.bid = bid
                p.save(update_fields=['bid'])

                context = {'msg': f'You Have successufully bidded this item for ${ bid } <a href="listing?q={itemId}">Go back</a>'}
                return render(request, "auctions/listing.html", context)

            except Bid.DoesNotExist:
                Bid.objects.create(user=request.user, item=Listing.objects.get(item=itemId), bid=bid)
                context = {'msg': f'You Have successufully bidded this item for ${ bid } <a href="listing?q={itemId}">Go back</a>'}
                return render(request, "auctions/listing.html", context)

        # add to watchlist
        except:
            try:
                id = request.POST['addLid']
                add = Watchlist(user=request.user, item=Item.objects.get(pk=id))
                add.save()
                    
                return HttpResponse("Added to watchlist !")
                
            # remove from watchlist
            except:
                try:
                    request.POST['reLid']
                    id = request.POST['reLid']
                    Watchlist.objects.filter(user=request.user, item=Item.objects.get(pk=id)).delete()
                
                    return HttpResponse("Removed from watchlist !")
                
                # add comment
                except:
                    request.POST['comment']
                    comment = request.POST['comment']
                    itemId = request.POST['itemId']
                    add = Comment(item=Item.objects.get(pk=itemId), user=request.user, comment=comment)
                    add.save()

                    return HttpResponse("comment added successfully")


    # single listing view through get
    id = request.GET['q']
    
    # if item is alreadyly in the watchlist then yes is sent 
    # which means it should display the remove from watchlist button else do otherwise
    watchlist = Watchlist.objects.filter(user=request.user, item=id)
    w=''
    if watchlist:
        w = 'yes'
    else:
        w = 'no'

    # total bid
    res = Listing.objects.get(item =id)
    item = res.id

    total_bids = Bid.objects.filter(item=item).count()

    # bid winner
    bid_winner = ''
    res = Bid.objects.filter(item=item)
    bw = [b.user for b in res][-1]
    if bw == request.user:
        bid_winner = 'You'
    else:
        bid_winner = bw

    # Total comments
    total_comments = Comment.objects.filter(item=id).count()
    
    # comments
    comments = Comment.objects.filter(item=id).order_by('-pk')

    # listings
    listings = Listing.objects.filter(item=id).order_by('-pk')
    for listing in listings:

        # for min value of bid input field
        current_bid = listing.current_bid + 1
        author = User.objects.filter(username=listing.author)

        context = {
            'listings': listings,
            'author': author,
            'current_bid': current_bid,
            'itemId': id,
            'w': w,
            'comments': comments,
            'total_comments': total_comments,
            'total_bids': total_bids,
            'bid_winner': bid_winner
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
