from django.shortcuts import render
from . models import *
from django.contrib import messages

def home(request):
    return render(request,"market/index.html")
def register(request):
    return render(request,"market/register.html")
def category(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"market/category.html",{"catagory":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"market/products/index.html",{"products":products})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('category')

