from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createListing", views.createListing, name="createListing"),
    path("categories", views.categories, name="categories"),
    path("category", views.category, name="category"),
    path("myListings", views.myListings, name="myListings"),
    path("closeL", views.closeL, name="closeL")
]
