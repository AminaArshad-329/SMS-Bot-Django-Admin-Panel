from django.urls import path
from .views import analytics_dashboard, UserLoginView, logout_view, orders_management, plans_management, users_management, admin_management

urlpatterns = [
    path('analytics', analytics_dashboard, name='Analytics'),
    path('', UserLoginView.as_view(), name='login'),
    path('orders/', orders_management, name='orders_management'),
    path('plans/', plans_management, name='plans_management'),
    path('users/', users_management, name='users_management'),
    path('admin_management/', admin_management, name='admin_management'),




    path('logout/', logout_view, name='logout'),
]
