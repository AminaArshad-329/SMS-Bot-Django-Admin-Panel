from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100, null = True, blank=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.username
    
class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=255)


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    inactive = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class PaymentGateway(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    api_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='orders')
    payment_gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('abandon', 'Abandon'),
        ('checkout', 'Checkout'),

    ))

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

# New models for additional statistics
class WebsiteVisitor(models.Model):
    date = models.DateField()
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Sale(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class MRR(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class ActiveSubscriber(models.Model):
    date = models.DateField()
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Unsubscriber(models.Model):
    date = models.DateField()
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
