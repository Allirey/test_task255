from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


class CartAdd(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])

        return redirect('cart:cart_detail')


class CartRemove(View):
    def get(self, request, product_id):
        print(product_id)
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)

        return redirect('cart:cart_detail')


class CartDetail(DetailView):
    template_name = 'cart/detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

        return cart
