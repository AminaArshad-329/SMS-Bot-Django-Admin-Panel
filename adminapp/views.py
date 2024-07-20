# adminapp/views.py
from rest_framework import generics
from .models import User, Plan, Subscription, PaymentGateway, Order, WebsiteVisitor, Sale, MRR, ActiveSubscriber, Unsubscriber
from .serializers import UserSerializer, PlanSerializer, SubscriptionSerializer, PaymentGatewaySerializer, OrderSerializer, WebsiteVisitorSerializer, SaleSerializer, MRRSerializer, ActiveSubscriberSerializer, UnsubscriberSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PlanListCreateView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class PaymentGatewayListCreateView(generics.ListCreateAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class WebsiteVisitorListCreateView(generics.ListCreateAPIView):
    queryset = WebsiteVisitor.objects.all()
    serializer_class = WebsiteVisitorSerializer

class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class MRRListCreateView(generics.ListCreateAPIView):
    queryset = MRR.objects.all()
    serializer_class = MRRSerializer

class ActiveSubscriberListCreateView(generics.ListCreateAPIView):
    queryset = ActiveSubscriber.objects.all()
    serializer_class = ActiveSubscriberSerializer

class UnsubscriberListCreateView(generics.ListCreateAPIView):
    queryset = Unsubscriber.objects.all()
    serializer_class = UnsubscriberSerializer
