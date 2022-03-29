from django.contrib import admin
from . models import User, Create, Comment,  BIDDING, CATEGORY,  mywatchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Create)
admin.site.register( Comment)
admin.site.register(BIDDING)
admin.site.register( CATEGORY)
admin.site.register( mywatchlist)

