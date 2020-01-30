from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from django.urls import reverse
from django.conf import settings
from coingate.client import CoinGateV2Client


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm(initial={'first_name': "John Doe"})
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def order_list(request):
    client = CoinGateV2Client(settings.COIN_GATE_APP_ID, settings.COIN_GATE_AUTH_TOKEN)
    orders = list(client.iterate_all_orders())

    return render(request, 'orders/order/list.html', {'orders': orders})
