from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    DeveloperDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    LoginView,
    RegistrationView,
    OrdersView,
    UserSettingsView,
    SearchView,
    MailingView,
    CheckoutView,
    MakeOrderView,
    PayedOnlineOrderView
)

urlpatterns = [
    path('', BaseView.as_view(), name='main'),
    path('products/<str:slug>', ProductDetailView.as_view(), name='product'),
    path('category/<str:slug>', CategoryDetailView.as_view(), name='category'),
    path('developer/<str:slug>', DeveloperDetailView.as_view(), name='developer'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>', ChangeQTYView.as_view(), name='change_qty'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('user-settings/', UserSettingsView.as_view(), name='user_settings'),
    path('search/', SearchView.as_view(), name='search'),
    path('mailing/', MailingView.as_view(), name='mailing'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('payed-online-order/', PayedOnlineOrderView.as_view(), name='payed_online_order'),
]