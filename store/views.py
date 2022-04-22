from django import views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render ,HttpResponse, get_object_or_404 
from django.views import View
from django.contrib import messages
from .models import Address, Collection, Product, Customer, Cart ,CartItem, Order,OrderItem
from .forms import CustomerRegistrationForm ,AddAddressForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from decimal import *
# # Create your views here.

def product_list(request):
    if(request.method== "POST"):
        x= request.POST.get("order_by",False)
        if (x==False):
            sortby='-last_update'
        else:
            if(x== "newest"):
                x='-last_update'
            sortby=x
    else:
        sortby='-last_update'
    products=Product.objects.order_by(sortby)
    products=list(products)
    
    data={
        "products":products,
        "recent_product":products[:3]
    }

    return render(request , "home.html",data)
    # return HttpResponse(list(querySet))


# def create_product(request):
#     if request.method == "POST":
#         data=request.POST
#         print(data)
#         return HttpResponse("done")

@login_required
def product_detail(request, id):
    try:
        product=Product.objects.get(pk=id)
 
        context={
            "product":product
        }
        return render(request,"product_detail.html",context)
    except:
        return HttpResponse("product does not exist <br> 404")

def searchProduct(request):
    search_term=request.GET.get("search")
    products=Product.objects.filter(title=search_term)
    return render(request, "search.html", {"products":products})


class customerRegistration(View):
    def get(self , request):
        form= CustomerRegistrationForm()
        return render(request,"auth/customerRegistration.html",{"form":form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]
            id=form.cleaned_data["id"]
            cus=Customer()
            cus.user=id
            cus.save()
        return render(request,"auth/customerRegistration.html", {"form":form})

@login_required
def profile(request):
    customer=Customer.objects.get(user=request.user)
    return render(request, "profile.html",{"customer":customer})

def category(request,id):
    if(request.method== "POST"):
        x= request.POST.get("order_by",False)
        if (x==False):
            sortby='-last_update'
        else:
            if(x== "newest"):
                x='-last_update'
            sortby=x
    else:
        sortby='-last_update'
    category_products=Product.objects.select_related("collection").filter(collection=id).order_by(sortby)

    return render(request , "category_products.html",{"products": category_products,"category_id":id})

class addressBook(View):
    def get(self,request):
        form=AddAddressForm()
        add=Address.objects.filter(customer=Customer.objects.get(user=request.user) )
        return render(request,'address_book.html',{'form':form ,'add':add})

    def post(self,request):
        form=AddAddressForm(request.POST)
        customer=Customer.objects.get(user=request.user)
        if form.is_valid():
            street=form.cleaned_data['street']
            city=form.cleaned_data['city']
            # reg=Customer(customer=user,street=street,city=city)
            reg= Address()
            reg.street=street
            reg.city=city
            reg.customer= customer
            reg.save()
            messages.success(request,' Address added successfully!')
        add=Address.objects.filter(customer=customer )
        return render(request,'address_book.html',{'form':form ,'add':add})


def createCart(request):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        reg=Cart()
        reg.customer=customer
        reg.save()
        return HttpResponse(reg.id)
    else:
        reg=Cart()
        reg.save()
        return HttpResponse(reg.id)
@csrf_exempt
def addToCart(request):
    if request.method =="POST":
        
        print("yolo!!!!!!!!!!!!!!!!!!!!")
        cartId= request.POST.get('cartId')
        productId= request.POST.get('productId')
        quantity= request.POST.get('quantity')
        
        cart=Cart.objects.get(pk=cartId)
        if request.user.is_authenticated:
            customer=Customer.objects.get(user=request.user)
            cart.customer=customer
            cart.save()
        product=Product.objects.get(pk=productId)
        reg=CartItem()
        reg.cart=cart
        reg.product=product
        reg.quantity=quantity
        reg.save()
        messages.SUCCESS("Product Addred to Cart!")
    return HttpResponse("Product Added to Cart!")

def cart(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    cart=Cart.objects.get(customer=customer)
    cartItems=CartItem.objects.filter(cart=cart)
    cartItems=list(cartItems)
    
    getcontext().prec = 2
    subTotal=Decimal(0)
    for x in cartItems:
        y=x.get_total_price()
        subTotal=subTotal+y
    return render(request,'cart.html',{"items":cartItems, "subTotal":subTotal})

@login_required
def checkout(request):
    if request.user.is_authenticated:
        user=request.user
        customer=Customer.objects.get(user=user)
        cart=Cart.objects.get(customer=customer)
        cartItems=CartItem.objects.filter(cart=cart)
        cartItems=list(cartItems)

        getcontext().prec = 2
        subTotal=Decimal(0)
        for x in cartItems:
            y=x.get_total_price()
            subTotal=subTotal+y
        add=Address.objects.filter(customer=customer)[0]
        return render(request, "checkout.html",{"items":cartItems, "subTotal":subTotal , "add":add})
    else:
        return redirect('login')

def placeOrder(request):
        if request.user.is_authenticated:
            user=request.user
            customer=Customer.objects.get(user=user)
            cart=Cart.objects.get(customer=customer)
            cartItems=CartItem.objects.filter(cart=cart)

            order= Order()
            order.customer=customer
            order.save()
            

            for c in cartItems:
                OrderItem(order=order,product=c.product,quantity=c.quantity ,unit_price=c.product.unit_price).save()
                
            cart.delete()
            context= {
                "order_id":order.id,
            }
        return render(request,"order_placed.html",context)

def myOrders(request):
    if request.user.is_authenticated:
        user=request.user
        customer = Customer.objects.get(user=user)    
        orders=Order.objects.filter(customer=customer).order_by("-placed_at")
        add=Address.objects.filter(customer=customer)[0]
        
        
    return render(request, "my_orders.html",{"orders":orders,"add":add})

def orderDetail(request,id):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        order=Order.objects.get(pk=id)
        
        order_items=OrderItem.objects.filter(order=order)
        orderItems=list(order_items)

        getcontext().prec = 2
        subTotal=Decimal(0)
        for x in orderItems:
            y=x.get_total_price()
            subTotal=subTotal+y
        add=Address.objects.filter(customer=customer)[0]
        return render(request, "order_detail.html",{"items":orderItems, "subTotal":subTotal , "add":add})
    else:
        return redirect('login')
    # if request.user.is_authenticated:
    #     order=Order.objects.get(pk=id)
    #     order_items=OrderItem.objects.filter(order=order)

    #     return HttpResponse(order_items)
