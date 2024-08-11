from django.urls import path
from market import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('category',views.category,name="category"),
    path('category/<str:name>',views.collectionsview,name="category"),
    path('category/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('payment', views.payment_page, name="payment"),
    path('payment/success', views.payment_success, name="payment_success"),
    path('payment/failure', views.payment_failure, name="payment_failure"),
    path('card-details/<int:order_id>/', views.card_details, name='card_details'),
]
