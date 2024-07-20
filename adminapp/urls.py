# adminapp/urls.py
from django.urls import path
from .views import (
    UserListCreateView, PlanListCreateView, SubscriptionListCreateView,
    PaymentGatewayListCreateView, OrderListCreateView, WebsiteVisitorListCreateView,
    SaleListCreateView, MRRListCreateView, ActiveSubscriberListCreateView, UnsubscriberListCreateView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('plans/', PlanListCreateView.as_view(), name='plan-list-create'),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription-list-create'),
    path('payment_gateways/', PaymentGatewayListCreateView.as_view(), name='payment-gateway-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('website_visitors/', WebsiteVisitorListCreateView.as_view(), name='website-visitor-list-create'),
    path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    path('mrr/', MRRListCreateView.as_view(), name='mrr-list-create'),
    path('active_subscribers/', ActiveSubscriberListCreateView.as_view(), name='active-subscriber-list-create'),
    path('unsubscribers/', UnsubscriberListCreateView.as_view(), name='unsubscriber-list-create'),
]
