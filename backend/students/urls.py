
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_page, name='logout'),

    # Dashboard routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Existing student routes
    path('student-form/', views.student_form, name='student_form'),
    path('student-list/', views.student_list, name='student_list'),

    # Ecommerce routes
    path('products/', views.products, name='products'),
]

