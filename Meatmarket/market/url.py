from django.urls import path
from market import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('register',views.register,name="register"),
    path('category',views.category,name="category"),
    path('category/<str:name>',views.collectionsview,name="category"),
    path('category/<str:cname>/<str:pname>',views.product_details,name="product_details"),
]
