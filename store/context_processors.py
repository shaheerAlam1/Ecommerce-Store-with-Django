from .models import Collection, Customer,Cart,CartItem
from django.db.models import Count

def CollectionContext(request):
    collection=Collection.objects.all()
    return {"collection": collection}

def CurrencyContext(request):
    return {"currency":"RS"}

# def CartCountContext(request):
#         if request.user.is_authenticated:
#             user=request.user
#             customer=Customer.objects.get(user=user)
#             cart=Cart.objects.get(customer=customer)
#             cart_count=CartItem.objects.filter(cart=cart).aggregate(Count("id"))
#             print(cart_count,"!!!!!!!!!!!!!!!!!!!!!!")
#             cart_count=cart_count["id__count"]
#             return {"cart_count":cart_count}
#         else:
#             return{"cart_count":""}
    
