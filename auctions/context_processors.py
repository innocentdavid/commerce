from django.contrib.auth import authenticate, login, logout

from .models import *

def watchlist_processor(request):
    watchlist = Watchlist.objects.filter(user=request.user).count()
    
    return {'total_watchlist': watchlist}