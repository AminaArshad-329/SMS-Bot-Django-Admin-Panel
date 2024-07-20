# adminapp/serializers.py
from rest_framework import serializers
from .models import User, Plan, Subscription, PaymentGateway, Order, WebsiteVisitor, Sale, MRR, ActiveSubscriber, Unsubscriber

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class WebsiteVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteVisitor
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class MRRSerializer(serializers.ModelSerializer):
    class Meta:
        model = MRR
        fields = '__all__'

class ActiveSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveSubscriber
        fields = '__all__'

class UnsubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unsubscriber
        fields = '__all__'
