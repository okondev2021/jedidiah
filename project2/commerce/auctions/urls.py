from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.new_list, name="create"),
    path('category', views.category1,name = "category"),
    path('watchlist', views.watchlist,name = "watchlist"),
    path('watchlists/<int:watchlistinfo>',views.watchlistinfo,name = 'watchlistinfo'),
    path('<int:list>',views.listings,name="listings"),
    path('category/<str:name>',views.cartname,name = "cartname"),

]
