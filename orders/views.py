from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from coingate.client import CoinGateV2Client


class OrderCreate(TemplateView):
    template_name = 'orders/order/create.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(initial={'first_name': "John Doe"})

        return render(request, self.template_name, {'cart': cart, 'form': form})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)

        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))


class OrderList(TemplateView):
    template_name = 'orders/order/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client = CoinGateV2Client(settings.COIN_GATE_APP_ID, settings.COIN_GATE_AUTH_TOKEN)
        orders = list(client.iterate_all_orders())
        context['orders'] = orders

        return context
