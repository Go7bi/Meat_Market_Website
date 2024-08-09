from django.urls import path
from market import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    path('category',views.category,name="category"),
    path('category/<str:name>',views.collectionsview,name="category"),
    path('category/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
]
