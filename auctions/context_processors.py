from django.contrib.auth import authenticate, login, logout

from .models import *

def watchlist_processor(request):
    try:
        watchlist = Watchlist.objects.filter(user=request.user).count()
    
        return {'total_watchlist': watchlist}
    except:
        return {'total_watchlist': 0}