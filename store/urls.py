from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm ,MyPasswordResetForm, MyPasswordChangeForm,MySetPasswordForm
from . import views
urlpatterns = [
    path("", views.product_list,name=""),
    path("product", views.product_list),
    path('product/<int:id>/', views.product_detail,name="product"),
    # path('create_products/', views.product_detail),

    path('search/',views.searchProduct, name='search'),
    path('cart/',views.cart,name="cart"),
    path('category/<int:id>',views.category,name='category_products'),
    path('create-cart/', views.createCart , name='create_cart'),
    path("add-to-cart/",views.addToCart,name="addToCart"),
    path("profile/", views.profile, name="profile"),
    path("address-book", views.addressBook.as_view(),name="address_book"),
    path("my-orders",views.myOrders,name="my_orders"),
    path("my-orders/<int:id>" ,views.orderDetail,name='order_detail'),
    path("checkout/",views.checkout,name="checkout"),
    path("place-order/",views.placeOrder,name="placeOrder"),

    
    path("register",views.customerRegistration.as_view(),name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html',authentication_form=LoginForm), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='auth/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/password-changed/'),name='passwordchange'),
    path('password-changed/',auth_views.PasswordChangeDoneView.as_view(template_name='auth/passwordchangedone.html'),name='passwordchangedone'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),name='password_reset_complete'),
    ]
