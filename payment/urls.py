from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.PaymentProcess.as_view(), name='process'),
    path('done/', views.PaymentDone.as_view(), name='done'),
    path('canceled/', views.PaymentCanceled.as_view(), name='canceled'),
]