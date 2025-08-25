from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.payment_webhook, name="payment_webhook"),
]