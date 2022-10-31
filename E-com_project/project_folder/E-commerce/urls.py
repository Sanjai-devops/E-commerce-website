from django.urls import path
from . import views

urlpatterns= [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fav_id>',views.remove_fav,name="remove_fav"),
    path('remove_cart/<str:cart_id>',views.remove_cart,name="remove_cart"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionview,name="collections"),
    path('collections/<str:catagory_name>/<str:product_name>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
]
