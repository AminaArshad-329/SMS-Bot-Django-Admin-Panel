from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import plotly.graph_objs as go
from plotly.offline import plot
from django.db.models import Count, Sum, F
from django.utils import timezone
from datetime import timedelta
from adminapp.models import Order, User, Plan, Subscription, PaymentGateway, WebsiteVisitor, Sale, MRR, ActiveSubscriber, Unsubscriber, Interest
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.core.paginator import Paginator
from .forms import AdminUserCreationForm
from django.contrib.auth import get_user_model


@login_required
def analytics_dashboard(request):
    date_filter = request.GET.get('date_filter', '30')
    if date_filter == '7':
        start_date = timezone.now() - timedelta(days=7)
    elif date_filter == '1':
        start_date = timezone.now() - timedelta(days=1)
    else:
        start_date = timezone.now() - timedelta(days=30)

    # Fetch and filter data based on the selected date range
    orders = Order.objects.filter(created_at__gte=start_date)
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('amount'))['amount__sum'] or 0
    orders_by_status = orders.values('status').annotate(count=Count('id'))

    # Line chart data for orders
    orders_by_date = orders.annotate(date=F('created_at__date')).values('date').annotate(count=Count('id')).order_by('date')
    dates = [order['date'] for order in orders_by_date]
    counts = [order['count'] for order in orders_by_date]

    # Fetch other stats data
    website_visitors = WebsiteVisitor.objects.filter(date__gte=start_date).order_by('date')
    live_website_visitors = WebsiteVisitor.objects.filter(date__gte=timezone.now() - timedelta(minutes=10)).count()

    sales = Sale.objects.filter(date__gte=start_date).order_by('date')
    mrr = MRR.objects.filter(date__gte=start_date).order_by('date')
    active_subscribers = ActiveSubscriber.objects.filter(date__gte=start_date).order_by('date')
    unsubscribers = Unsubscriber.objects.filter(date__gte=start_date).order_by('date')

    mrr_count = mrr.count()
    active_subscribers_count = active_subscribers.count()
    unsubscribers_count = unsubscribers.count()
    website_visitors_count = website_visitors.count()

    # Helper function to extract dates and values for plotting
    def extract_dates_and_values(queryset, value_field):
        return [item.date for item in queryset], [getattr(item, value_field) for item in queryset]

    visitor_dates, visitor_counts = extract_dates_and_values(website_visitors, 'count')
    sale_dates, sale_amounts = extract_dates_and_values(sales, 'amount')
    mrr_dates, mrr_amounts = extract_dates_and_values(mrr, 'amount')
    active_subscriber_dates, active_subscriber_counts = extract_dates_and_values(active_subscribers, 'count')
    unsubscriber_dates, unsubscriber_counts = extract_dates_and_values(unsubscribers, 'count')

    # Custom fill color and line color
    fill_color = 'rgba(173, 216, 230, 0.5)'  # Lighter blue color with 50% opacity
    line_color = 'rgba(37, 150, 190, 1)'  # Custom line color

    # Generate plots with only horizontal grid lines
    def create_fig(x, y, title):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', mode='lines', fillcolor=fill_color, line=dict(color=line_color)))
        fig.update_layout(
            title=title,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(192, 192, 192, 0.4)'  # Darker grey grid lines
            )
        )
        return fig

    fig_website_visitors = create_fig(visitor_dates, visitor_counts, 'Website Visitors')
    fig_sales = create_fig(sale_dates, sale_amounts, 'Sales')
    fig_mrr = create_fig(mrr_dates, mrr_amounts, 'Monthly Recurring Revenue (MRR)')
    fig_active_subscribers = create_fig(active_subscriber_dates, active_subscriber_counts, 'Active Subscribers')
    fig_unsubscribers = create_fig(unsubscriber_dates, unsubscriber_counts, 'Unsubscribers')

    plot_website_visitors = plot(fig_website_visitors, output_type='div')
    plot_sales = plot(fig_sales, output_type='div')
    plot_mrr = plot(fig_mrr, output_type='div')
    plot_active_subscribers = plot(fig_active_subscribers, output_type='div')
    plot_unsubscribers = plot(fig_unsubscribers, output_type='div')
    checkout_count = Order.objects.filter(status='checkout').count()
    abandon_count = Order.objects.filter(status='abandon_count').count()
    # Query all users, annotate their locations, and order by count descending
    user_locations = User.objects.exclude(location__isnull= True).values('location').annotate(count=Count('location')).order_by('-count')[:5]
    # Create a dictionary to store the location and their counts
    location_dict = {entry['location']: entry['count'] for entry in user_locations}


    context = {
        'date_filter': date_filter,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'plot_website_visitors': plot_website_visitors,
        'plot_sales': plot_sales,
        'plot_mrr': plot_mrr,
        'plot_active_subscribers': plot_active_subscribers,
        'plot_unsubscribers': plot_unsubscribers,
        'mrr': mrr_count,
        'active_subscribers': active_subscribers_count,
        'unsubscribers': unsubscribers_count,
        'website_visitors': website_visitors_count,
        'live_website_visitors': live_website_visitors,
        'checkout_count' : checkout_count,
        'abandon_count' :abandon_count,
        'location_dict' : location_dict
    }

    return render(request, 'dashboard.html', context)


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = 'Analytics'  # Ensure this matches the name of the URL pattern

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Analytics')
        return super().get(request, *args, **kwargs)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from adminapp.models import Order, User, Plan, Subscription, PaymentGateway, WebsiteVisitor, Sale, MRR, ActiveSubscriber, Unsubscriber
from django.core.paginator import Paginator
import plotly.graph_objs as go
from plotly.offline import plot

@login_required
def orders_management(request):
    date_filter = request.GET.get('date_filter', '30')
    if date_filter == '7':
        start_date = timezone.now() - timedelta(days=7)
    elif date_filter == '1':
        start_date = timezone.now() - timedelta(days=1)
    else:
        start_date = timezone.now() - timedelta(days=30)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        return redirect('orders_management')

    # Fetch and filter data based on the selected date range
    orders = Order.objects.filter(created_at__gte=start_date)
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    completed_orders = orders.filter(status='completed').count()
    orders_by_status = orders.values('status').annotate(count=Count('id'))

    # Line chart data for orders over time
    orders_by_date = orders.annotate(date=F('created_at__date')).values('date').annotate(count=Count('id')).order_by('date')
    dates = [order['date'] for order in orders_by_date]
    counts = [order['count'] for order in orders_by_date]

    # Total revenue from orders
    total_revenue = orders.aggregate(Sum('amount'))['amount__sum'] or 0
    revenue_by_date = orders.annotate(date=F('created_at__date')).values('date').annotate(total=Sum('amount')).order_by('date')
    revenue_dates = [revenue['date'] for revenue in revenue_by_date]
    revenue_totals = [revenue['total'] for revenue in revenue_by_date]

    # Custom fill color and line color
    fill_color = 'rgba(173, 216, 230, 0.5)'  # Lighter blue color with 50% opacity
    line_color = 'rgba(37, 150, 190, 1)'  # Custom line color

    # Generate plots with only horizontal grid lines
    def create_fig(x, y, title):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', mode='lines', fillcolor=fill_color, line=dict(color=line_color)))
        fig.update_layout(
            title=title,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(192, 192, 192, 0.4)'  # Darker grey grid lines
            )
        )
        return fig

    fig_orders_by_status = go.Figure(data=[
        go.Bar(x=[status['status'] for status in orders_by_status], y=[status['count'] for status in orders_by_status])
    ])
    fig_orders_by_status.update_layout(title='Orders by Status', plot_bgcolor='white', paper_bgcolor='white', yaxis=dict(showgrid=True, gridcolor='rgba(192, 192, 192, 0.4)'))

    fig_orders_over_time = create_fig(dates, counts, 'Orders Over Time')
    fig_revenue_from_orders = create_fig(revenue_dates, revenue_totals, 'Revenue from Orders')

    plot_orders_by_status = plot(fig_orders_by_status, output_type='div')
    plot_orders_over_time = plot(fig_orders_over_time, output_type='div')
    plot_revenue_from_orders = plot(fig_revenue_from_orders, output_type='div')
    orders = Order.objects.all()
    paginator = Paginator(orders, 10)  # Show 10 orders per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'date_filter': date_filter,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'plot_orders_by_status': plot_orders_by_status,
        'plot_orders_over_time': plot_orders_over_time,
        'plot_revenue_from_orders': plot_revenue_from_orders,
        'page_obj': page_obj,
        'statuses': Order._meta.get_field('status').choices
    }

    return render(request, 'orders.html', context)


@login_required
def plans_management(request):
    date_filter = request.GET.get('date_filter', '30')
    if date_filter == '7':
        start_date = timezone.now() - timedelta(days=7)
    elif date_filter == '1':
        start_date = timezone.now() - timedelta(days=1)
    else:
        start_date = timezone.now() - timedelta(days=30)

    if request.method == 'POST':
        for plan in Plan.objects.all():
            plan_id = plan.id
            if f'save_{plan_id}' in request.POST:
                plan.price = request.POST.get(f'price_{plan_id}')
                plan.duration_in_days = request.POST.get(f'duration_{plan_id}')
                plan.inactive = request.POST.get(f'status_{plan_id}') == 'True'
                plan.save()
                return redirect('plans_management')

    plans = Plan.objects.filter(created_at__gte=start_date)
    total_plans = plans.count()
    active_plans = plans.exclude(inactive=True).count()
    expired_plans = plans.filter(inactive=True).count()
    
    plans = Plan.objects.all()
    paginator = Paginator(plans, 10)  # Show 10 plans per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'date_filter': date_filter,
        'total_plans': total_plans,
        'active_plans': active_plans,
        'expired_plans': expired_plans,
        'page_obj': page_obj
    }

    return render(request, 'plans.html', context)

def users_management(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)  # Show 10 users per page

    if request.method == 'POST':
        for user in users:
            user_id = user.id
            if f'save_{user_id}' in request.POST:
                user.first_name = request.POST.get(f'first_name_{user_id}')
                user.last_name = request.POST.get(f'last_name_{user_id}')
                user.email = request.POST.get(f'email_{user_id}')
                user.save()
                return redirect('users_management')

            if f'add_interest_{user_id}' in request.POST:
                interest_name = request.POST.get(f'new_interest_{user_id}')
                if interest_name:
                    Interest.objects.create(user=user, name=interest_name)
                return redirect('users_management')

            if 'remove_interest' in request.POST:
                value = request.POST.get('remove_interest')
                user_id, interest_id = value.split('-')
                Interest.objects.filter(id=interest_id, user_id=user_id).delete()
                return redirect('users_management')

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'users.html', context)

User = get_user_model()


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_management(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_management')
    else:
        form = AdminUserCreationForm()

    users = User.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj
    }

    return render(request, 'admin_management.html', context)