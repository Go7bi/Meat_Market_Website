from django.http import  JsonResponse
from django.shortcuts import redirect, render
from market.forms import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from market.forms import PaymentForm
from .forms import CardForm

def home(request):
    products = Product.objects.filter(trending = 1)
    return render(request,"market/index.html",{'products':products})

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")

def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"market/login.html")

def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"market/cart.html",{"cart":cart})
  else:
    return redirect("/")

def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"market/fav.html",{"fav":fav})
  else:
    return redirect("/")
  
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")

def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"market/register.html",{'form':form})

def category(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"market/category.html",{"catagory":catagory})

def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"market/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('category')

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
      if(Product.objects.filter(name=pname,status=0)):
        products=Product.objects.filter(name=pname,status=0).first()
        return render(request,"market/products/product_details.html",{"products":products})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('category')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('category')
    

def payment_page(request):
    cart = Cart.objects.filter(user=request.user)
    total = sum([item.total_cost for item in cart])
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = Order()
            order.user = request.user
            order.name = form.cleaned_data['name']
            order.email = form.cleaned_data['email']
            order.phone = form.cleaned_data['phone']
            order.address = form.cleaned_data['address']
            order.payment_method = form.cleaned_data['payment_method']
            order.total = total
            if order.payment_method == 'online':  # Check if payment method is online
              order.save()  # Save the order object here
              return redirect('card_details', order_id=order.id)
            
            
            else:
                order.save()
                for item in cart:
                    item.delete()
                return redirect("payment_success")
        else:
            return redirect("payment_failure")
    else:
        form = PaymentForm()
    return render(request, "market/payment.html", {"cart": cart, "total": total, "form": form})



def card_details(request, order_id):
    order = Order.objects.get(id=order_id)
    cart = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CardForm(request.POST)
        order.save()
        for item in cart:
            item.delete()
        return redirect("payment_success")  # Move the return statement here
    else:
        form = CardForm()
        return render(request, 'market/card_details.html', {'form': form, 'order': order})
    
def payment_success(request):
    return render(request, 'market/payment_success.html')



def payment_failure(request):
    return render(request, "market/payment_failure.html")

def search_products(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(name__icontains=query)
            return render(request, 'market/search_results.html', {'products': products})
        else:
            return render(request, 'market/search.html', {'form': form})
    else:
        form = SearchForm()
        return render(request, 'market/search.html', {'form': form})

def search_results(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'market/search_results.html', {'products': products, 'query': query})
