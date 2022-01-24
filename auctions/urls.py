from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.auction_listing, name="auction_listing"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category, name="category"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("won_auctions", views.won_auctions,name="won_auctions"),
    path("listed_auctions",views.listed_auctions,name="listed_auctions"),
]
