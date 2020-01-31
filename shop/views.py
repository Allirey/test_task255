from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm
from django.views.generic import ListView, DetailView


class ProductList(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    extra_context = {}

    def get_queryset(self):
        products = Product.objects.filter(available=True)
        self.extra_context['category'] = None
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            self.extra_context['category'] = category

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_object(self, query_set=None):
        obj = get_object_or_404(Product, id=self.kwargs.get('id'), slug=self.kwargs.get('slug'), available=True)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
