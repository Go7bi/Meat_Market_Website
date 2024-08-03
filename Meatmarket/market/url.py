from django.urls import path
from market import views
urlpatterns = [
    path('home',views.home,name="home"),
    path('register',views.home,name="register")
]