# adminapp/admin.py
from django.contrib import admin
from .models import User, Plan, Subscription, PaymentGateway, Order, WebsiteVisitor, Sale, MRR, ActiveSubscriber, Unsubscriber

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_in_days')
    search_fields = ('name',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    search_fields = ('user__username', 'plan__name')
    list_filter = ('is_active', 'start_date', 'end_date')

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'payment_gateway', 'amount', 'transaction_id', 'status', 'created_at')
    search_fields = ('user__username', 'subscription__plan__name', 'transaction_id')
    list_filter = ('status', 'created_at')

@admin.register(WebsiteVisitor)
class WebsiteVisitorAdmin(admin.ModelAdmin):
    list_display = ('date', 'count', 'created_at')
    search_fields = ('date',)
    list_filter = ('date', 'created_at')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'created_at')
    search_fields = ('date',)
    list_filter = ('date', 'created_at')

@admin.register(MRR)
class MRRAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'created_at')
    search_fields = ('date',)
    list_filter = ('date', 'created_at')

@admin.register(ActiveSubscriber)
class ActiveSubscriberAdmin(admin.ModelAdmin):
    list_display = ('date', 'count', 'created_at')
    search_fields = ('date',)
    list_filter = ('date', 'created_at')

@admin.register(Unsubscriber)
class UnsubscriberAdmin(admin.ModelAdmin):
    list_display = ('date', 'count', 'created_at')
    search_fields = ('date',)
    list_filter = ('date', 'created_at')
