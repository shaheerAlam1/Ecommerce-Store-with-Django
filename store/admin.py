from django.contrib import admin
from .models import Collection , Promotion , Product , Customer , Address , Order , OrderItem , CartItem , Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Collection)
admin.site.register(Promotion)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(CartItem)
admin.site.register(Cart)
