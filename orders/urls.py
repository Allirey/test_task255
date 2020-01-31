from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreate.as_view(), name='order_create'),
    path('', views.OrderList.as_view(), name='list'),
]
