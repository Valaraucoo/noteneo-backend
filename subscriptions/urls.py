from django.urls import path, include
from .views.stripe import StripeWebhook, StripeActions, StripeSubscriptions
from .views.pages import SuccessPaymentView, FailedPaymentView

app_name = 'subscriptions'

urlpatterns = [
    path('stripe/', StripeWebhook.as_view(), name='stripe-webhook'),
    path('stripe/cancel/', StripeSubscriptions.as_view(), name='stripe-cancel'),
    path('stripe/session/', StripeActions.as_view(), name='stripe-actions'),
    path('success/', SuccessPaymentView.as_view(), name='success-payment'),
    path('failed/', FailedPaymentView.as_view(), name='success-payment'),
]
