from django.utils import timezone
from faker import Faker
import random

from adminapp.models import User, Plan, Subscription, PaymentGateway, Order, WebsiteVisitor, Sale, MRR, ActiveSubscriber, Unsubscriber

fake = Faker()

def create_dummy_data():
    def create_users(n):
        users = []
        for _ in range(n):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='password',
                location=fake.city()
            )
            users.append(user)
        return users

    def create_plans(n):
        plans = []
        for _ in range(n):
            plan = Plan.objects.create(
                name=fake.word(),
                description=fake.text(),
                price=random.uniform(10.0, 100.0),
                duration_in_days=random.randint(30, 365),
                created_at=timezone.now(),
                inactive=random.choice([True, False])
            )
            plans.append(plan)
        return plans

    def create_subscriptions(users, plans):
        subscriptions = []
        for user in users:
            plan = random.choice(plans)
            subscription = Subscription.objects.create(
                user=user,
                plan=plan,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=plan.duration_in_days),
                is_active=random.choice([True, False])
            )
            subscriptions.append(subscription)
        return subscriptions

    def create_payment_gateways(n):
        payment_gateways = []
        for _ in range(n):
            payment_gateway = PaymentGateway.objects.create(
                name=fake.company(),
                description=fake.text(),
                api_key=fake.uuid4()
            )
            payment_gateways.append(payment_gateway)
        return payment_gateways

    def create_orders(users, subscriptions, payment_gateways):
        orders = []
        for user in users:
            subscription = random.choice(subscriptions)
            payment_gateway = random.choice(payment_gateways)
            order = Order.objects.create(
                user=user,
                subscription=subscription,
                payment_gateway=payment_gateway,
                amount=subscription.plan.price,
                transaction_id=fake.uuid4(),
                created_at=timezone.now(),
                status=random.choice(['pending', 'completed', 'failed', 'abandon', 'checkout'])
            )
            orders.append(order)
        return orders

    def create_website_visitors(n):
        start_date = timezone.now() - timezone.timedelta(days=n)
        for i in range(n):
            date = start_date + timezone.timedelta(days=i)
            WebsiteVisitor.objects.create(
                date=date,
                count=random.randint(100, 500),
                created_at=timezone.now()
            )

    def create_sales(n):
        start_date = timezone.now() - timezone.timedelta(days=n)
        for i in range(n):
            date = start_date + timezone.timedelta(days=i)
            Sale.objects.create(
                date=date,
                amount=random.uniform(1000.0, 5000.0),
                created_at=timezone.now()
            )

    def create_mrr(n):
        start_date = timezone.now() - timezone.timedelta(days=n)
        for i in range(n):
            date = start_date + timezone.timedelta(days=i)
            MRR.objects.create(
                date=date,
                amount=random.uniform(10000.0, 50000.0),
                created_at=timezone.now()
            )

    def create_active_subscribers(n):
        start_date = timezone.now() - timezone.timedelta(days=n)
        for i in range(n):
            date = start_date + timezone.timedelta(days=i)
            ActiveSubscriber.objects.create(
                date=date,
                count=random.randint(200, 300),
                created_at=timezone.now()
            )

    def create_unsubscribers(n):
        start_date = timezone.now() - timezone.timedelta(days=n)
        for i in range(n):
            date = start_date + timezone.timedelta(days=i)
            Unsubscriber.objects.create(
                date=date,
                count=random.randint(10, 50),
                created_at=timezone.now()
            )

    users = User.objects.all()
    plans = Plan.objects.all()
    subscriptions = create_subscriptions(users, plans)
    payment_gateways = PaymentGateway.objects.all()
    create_orders(users, subscriptions, payment_gateways)
    create_website_visitors(30)
    create_sales(30)
    create_mrr(30)
    create_active_subscribers(30)
    create_unsubscribers(30)

# Run the function to create the dummy data
create_dummy_data()
