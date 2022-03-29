from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
import datetime
from django.contrib import messages
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import Create
from .models import User
from .models import Comment
from .models import BIDDING
from .models import CATEGORY
from .models import mywatchlist

def index(request):
    if request.method == "POST":
        fetch = request.POST['fetch']
        if fetch == 'All':
            Items = Create.objects.all()
        else:
            Items = Create.objects.filter(CATEGORY = fetch)
        return render(request, "auctions/index.html",{'Items':Items})

    else:
        wong =  Items = Create.objects.all()
        return render(request, "auctions/index.html",{'Items':wong})

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

@ login_required(login_url = "login" , redirect_field_name = 'next')
def new_list(request):
    time =datetime.date.today()
    if request.method=='POST':
        TITLE=request.POST['TITLE']
        DESCRIPTION=request.POST['DESCRIPTION']
        CATEGORY=request.POST['CATEGORY']
        BID=request.POST['BID']
        IMAGE=request.POST['IMAGE']
        TIME = time
        OWNER=request.POST['OWNER']
        BIDGATE =request.POST['BIDGATE']
        if TITLE=="" or DESCRIPTION =="" or CATEGORY=="" or BID=="" or IMAGE == "":
            messages.info(request,'Sorry, but u can only submit when all data has been entered')
        else:
            user= Create.objects.create(TITLE=TITLE,DESCRIPTION=DESCRIPTION,CATEGORY=CATEGORY,BID=BID,IMAGE=IMAGE,TIME=TIME,OWNER=OWNER,BIDGATE = BIDGATE)
            user.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")

    return render(request, "auctions/create.html")

# @ login_required(login_url = "login")
def listings(request,list, template =  "auctions/item.html"):
    biddin = BIDDING.objects.values_list('BIDS').filter(ITEM =list)
    comments= Comment.objects.filter(ITEM =list)
    biditem = BIDDING.objects.filter(ITEM =list)
    listing = Create.objects.get(id = list)
    bidding = BIDDING.objects.values_list('BIDS').filter(ITEM =list)
    biddname = BIDDING.objects.values_list('NAME').filter(ITEM =list)
    max_bidd = BIDDING.objects.filter(ITEM =list).aggregate(maxbid = Max('BIDS'))['maxbid']
    max_bid_name = BIDDING.objects.filter(ITEM =list).aggregate(maxbid = Max('BIDS'))['maxbid']
    maxy= BIDDING.objects.order_by('-BIDS').first()
    bidgate =  Create.objects.values_list('BIDGATE').filter(id = list)
    biddin_number = BIDDING.objects.values_list('BIDS').filter(ITEM =list)
    opens ='OPEN'
    closed = 'CLOSE'
    for bid_gate in bidgate:
        for biddgate in bid_gate:
            pass
    
    try:
        if request.method == 'POST':
            COMMENT = request.POST['comment']
            USER = request.POST['user']
            ITEM = request.POST['item_id']
            if COMMENT =="":
                messages.info(request,'no comment to save')
            else:
                user = Comment.objects.create(COMMENT = COMMENT,USER = USER,ITEM= ITEM)
                user.save()
 
    except:
        if 'send' in request.POST:
            BIDDS = request.POST['bidds']
            NAME = request.POST['bidder']
            ITEM = request.POST['bid_itemno']

            if BIDDS == "" :
                messages.info(request,'No bid has been placed')
            else:
                BIDD = int(BIDDS )
                try:
                    if BIDD <= listing.BID:
                        messages.info(request,f'Must be greater than startin bid ')
                    elif BIDD <= max_bidd:
                        messages.info(request,f'Must be greater than current highest bid')
                    else:
                        messages.info(request,f'Your bid has been received for {listing.TITLE}')
                        user = BIDDING.objects.create(BIDS = BIDDS , NAME = NAME, ITEM = ITEM)
                        user.save()

                except:
                    if BIDD <= listing.BID:
                        messages.info(request,f'Must be greater than startin bid ')
                    else:
                        messages.info(request,f'Your bid has been received for {listing.TITLE}')
                        user = BIDDING.objects.create(BIDS = BIDDS , NAME = NAME, ITEM = ITEM)
                        user.save()

        if 'close' in request.POST:
            messages.info(request,f'Bidding closed')
            Create.objects.filter(pk = list).update(BIDGATE ='CLOSED')

        if 'addwatchlist' in request.POST:
            auction_add = Create.objects.get(id = list)
            try:
                watchlist = mywatchlist.objects.get(user = request.user)
                if auction_add in watchlist.auctionitem.all():
                    watchlist.auctionitem.remove(auction_add)
                else:
                    watchlist.auctionitem.add(auction_add)
                    watchlist.save()
            except:
                a1 = mywatchlist(user = request.user)
                a1.save()
                watchlist = mywatchlist.objects.get(user = request.user)
                if auction_add in watchlist.auctionitem.all():
                    watchlist.auctionitem.remove(auction_add)
                else:
                    watchlist.auctionitem.add(auction_add)
                    watchlist.save()
    try:
        aucadd =  Create.objects.get(id = list)
        walist =  mywatchlist.objects.get(user = request.user)
        nn =  walist.auctionitem.all()
    except:
        a1 = mywatchlist(user = request.user)
        a1.save()
        aucadd =  Create.objects.get(id = list)
        walist =  mywatchlist.objects.get(user = request.user)
        nn =  walist.auctionitem.all()

    try:
        amount = []
        for bidds in biddin:
            for bider in bidds:
                amount.append(bider)
                amount.sort()
                light = amount[-1]
        high = f"Bidding for {listing.TITLE} ongoing,highest bidder with ${light}"
    except:
        high =  f"Initial amount : ${listing.BID}  No bid has been placed"

    return render(request, "auctions/item.html",{'listing':listing,'comments':comments,'bidding': bidding,'bidgate':biddgate,'opens':opens,'bidgate':bidgate,'closed':closed,'max_bid':maxy,'max_bidd':max_bidd,'high':high,'aucadd':aucadd,'nn':nn})
            

def category1(request):
    cart = CATEGORY.objects.all()
    return render(request, "auctions/category.html",{'cart':cart})

def cartname(request,name):
    categ = Create.objects.filter(CATEGORY = name)
    return render(request, "auctions/cartname.html",{'categ':categ})

def watchlist(request):
    try:
        check = mywatchlist.objects.get(user = request.user)
        checks =  check.auctionitem.all()
    except:
        a1 = mywatchlist(user = request.user)
        a1.save()
        check = mywatchlist.objects.get(user = request.user)
        checks =  check.auctionitem.all()
    return render(request, "auctions/watchlist.html",{'checks':checks})

def watchlistinfo(request,watchlistinfo):
    watchlist_detail = Create.objects.get(id = watchlistinfo)
    if request.method == 'POST': 
        watch_no = Create.objects.get(id = watchlistinfo)
        checkwatch = mywatchlist.objects.get(user = request.user)
        if watch_no in checkwatch.auctionitem.all():
            checkwatch.auctionitem.remove(watch_no)
            return HttpResponseRedirect(reverse('watchlist'))
    return render(request,"auctions/watchlistinfo.html",{"watchlist_detail":watchlist_detail}) 




