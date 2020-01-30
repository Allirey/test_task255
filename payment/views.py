from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from django.urls import reverse
from django.conf import settings
from coingate.client import CoinGateV2Client, CoinGateV2Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    client = CoinGateV2Client(settings.COIN_GATE_APP_ID, settings.COIN_GATE_AUTH_TOKEN)

    new_order = CoinGateV2Order.new(
        f"{order_id}",
        float(order.get_total_cost()),
        "USD",
        "USD",
        # callback_url='https://api.example.com/paymentcallback?token=randomtoken',
        cancel_url='http://127.0.0.1:8000' + reverse('payment:canceled'),
        success_url='http://127.0.0.1:8000' + reverse('payment:done')
    )
    placed_order = client.create_order(new_order)
    return redirect(placed_order.payment_url)


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
