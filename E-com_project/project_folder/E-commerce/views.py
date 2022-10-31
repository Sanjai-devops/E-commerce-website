from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render
from Ecommerce.form import Registering_Form
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.
def home(request):
    products=Product.objects.filter(trending_product=1)
    return render(request,'index.html',{"products":products})

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,'fav.html',{"fav":fav})
    else:
        return redirect("/")

def remove_fav(request,fav_id):
    item=Favourite.objects.get(id=fav_id)
    item.delete()
    return redirect("/favviewpage")         

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'cart.html',{"cart":cart})
    else:
        return redirect("/")

def remove_cart(request,cart_id):
    cartitem=Cart.objects.get(id=cart_id)
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
                    return JsonResponse({'status':'product Already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to Favourite'}, status=200)
           
        else:
            return JsonResponse({'status':'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'product Already in Cart'}, status=200)
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

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")    

def login_page(request):
     if request.user.is_authenticated:
        return redirect('/') 
     else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
               login(request,user)
               messages.success(request,"Logged in Successfully")
               return redirect('/') 
            else:
               messages.error(request,"Invalid User Name Or Password")
               return redirect("/login")           
        return render(request,'login.html')    

def register(request):
    form=Registering_Form()
    if request.method=='POST':
        form=Registering_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You can Login Now...!")
            return redirect('/login')
    return render(request,'Register.html',{"form":form})

def collections(request):
    Catagory=catagory.objects.filter(status=0)
    return render(request,'collections.html',{"catagory":Catagory})

def collectionview(request,name):
    if(catagory.objects.filter(name=name,status=0)):
       products=Product.objects.filter(category__name=name)
       return render(request,'products/index.html',{"products":products,"category_name":name})
    else: 
         messages.warning(request,"No Such Catagory Found")
         return redirect('collections')

def product_details(request,catagory_name,product_name):
   if(catagory.objects.filter(name=catagory_name,status=0)):
     if(Product.objects.filter(name=product_name,status=0)):
        products=Product.objects.filter(name=product_name,status=0).first()
        return render(request,"products/product_details.html",{"products":products})
     else:
        messages.error(request,"No Such Product Found")
        return redirect('collections')
   else: 
         messages.warning(request,"No Such Catagory Found")
         return redirect('collections')
