import stripe

from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import DetailView, View

from .models import Category, Developer, Customer, CartProduct, Product, Order, Cart, Mailing
from .mixins import CartMixin
from .forms import LoginForm, RegistrationForm, PasswordCustomChangeForm, MailingForm, OrderForm
from .utils import recalc_cart


past_page = None


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        new_products = Product.objects.all().order_by('-id')[:5]
        microsoft = Developer.objects.get(slug='microsoft')
        microsoft_products = Product.objects.filter(developer=microsoft)[:5]
        mailing_form = MailingForm(request.POST or None)
        context = {
            'new_products': new_products,
            'microsoft_products': microsoft_products,
            'cart': self.cart,
            'mailing_form': mailing_form
        }
        global past_page
        past_page = None
        return render(request, 'online_shop/index.html', context)


class ProductDetailView(CartMixin, DetailView):

    model = Product
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'online_shop/product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['past_page'] = past_page
        return context


class CategoryDetailView(CartMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'info'
    template_name = 'online_shop/catalog.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['info_products'] = Product.objects.filter(category=self.get_object())
        global past_page
        past_page = self.get_object()
        return context


class DeveloperDetailView(CartMixin, DetailView):

    model = Developer
    queryset = Developer.objects.all()
    context_object_name = 'info'
    template_name = 'online_shop/catalog.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['info_products'] = Product.objects.filter(developer=self.get_object())
        global past_page
        past_page = self.get_object()
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        else:
            cart_product.qty += 1
            cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect(product.get_absolute_url())


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):

        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
        }
        global past_page
        past_page = None
        return render(request, 'online_shop/cart.html', context)


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(None)
        context = {
            'form': form,
            'cart': self.cart
        }
        global past_page
        past_page = None
        return render(request, 'online_shop/enter.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'online_shop/enter.html', context)


class RegistrationView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart
        }
        global past_page
        past_page = None
        return render(request, 'online_shop/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'online_shop/registration.html', context)


class OrdersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer)
        context = {'orders': orders, 'cart': self.cart}
        return render(request, 'online_shop/orders.html', context)


class UserSettingsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = PasswordCustomChangeForm(request.POST or None)
        context = {
            'form': form,
            'cart': self.cart
        }
        global past_page
        past_page = None
        return render(request, 'online_shop/userSettings.html', context)

    def post(self, request, *args, **kwargs):
        form = PasswordCustomChangeForm(request.user, request.POST)
        successful_message = None
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            login(request, user)
            successful_message = "Пароль изменен"
        context = {'form': form, "successful_message": successful_message, 'cart': self.cart}
        return render(request, 'online_shop/userSettings.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51HzHvdIrVI4qAXnwFBIcIP7oRqH4CshFnIFhJJg89ZylLtWxmd4YNW0qzxq4X0Oh8ypiyVeJT6Ydy7jmdyL0VnJ80063E8Quo7"

        intent = stripe.PaymentIntent.create(
            amount=int(self.cart.final_price * 100),
            currency='rub',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )
        form = OrderForm(request.POST or None)
        context = {
            'cart': self. cart,
            'form': form,
            'client_secret': intent.client_secret
        }
        return render(request, 'online_shop/checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        user = request.user
        customer = Customer.objects.get(user=user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = user.first_name
            new_order.last_name = user.last_name
            new_order.phone = customer.phone
            new_order.email = user.email
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class PayedOnlineOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.get(user=user)
        new_order = Order()
        new_order.customer = customer
        new_order.first_name = user.first_name
        new_order.last_name = user.last_name
        new_order.phone = customer.phone
        new_order.email = user.email
        new_order.save()
        self.cart.in_order = True
        self.cart.save()
        new_order.cart = self.cart
        new_order.status = Order.STATUS_PAYED
        new_order.save()
        customer.orders.add(new_order)
        return JsonResponse({"status": "payed"})


class SearchView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        search = request.POST.get("search")
        info_products = Product.objects.filter(title__icontains=search)
        info = {
            "name": "Поиск"
        }
        context = {"info": info, "info_products": info_products}
        return render(request, 'online_shop/catalog.html', context)


class MailingView(View):

    def post(self, request, *args, **kwargs):
        form = MailingForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            Mailing.objects.create(email=email)
        messages.add_message(request, messages.ERROR, form.non_field_errors())
        return HttpResponseRedirect('/')

