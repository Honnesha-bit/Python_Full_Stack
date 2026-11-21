from django.shortcuts import render, redirect
from .form import studentform
from .models import students
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import product
from django.contrib.auth.models import User

from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone

from django.shortcuts import get_object_or_404

from .models import CartItem, WishlistItem, Order, OrderItem

@login_required(login_url='login')
def student_form(request):

    if request.method == 'POST':
        form = studentform(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = studentform()

    return render(
        request,
        'student/student_forms.html',
        {'form': form}
    )

@login_required(login_url='login')
def student_list(request):

    students = students.objects.all()

    return render(
        request,
        'student/student_list.html',
        {'students': students}
    )

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        else:
            return render(request, 'student/login.html', {
                'error': 'Invalid username or password. Please try again.'
            })

    return render(request, 'student/login.html')

@login_required(login_url='login')

# ==========================================
# DASHBOARD ROUTER
# ==========================================

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    return redirect('customer_dashboard')


# ==========================================
# CUSTOMER DASHBOARD
# ==========================================

@login_required(login_url='login')
def customer_dashboard(request):

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related('product')

    wishlist_items = WishlistItem.objects.filter(
        user=request.user
    ).select_related('product')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    cart_total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    recent_products = product.objects.filter(
        stock__gt=0
    ).order_by('-id')[:4]

    context = {
        'cart_items': cart_items,
        'cart_count': cart_items.count(),
        'cart_total': cart_total,
        'wishlist_count': wishlist_items.count(),
        'orders': orders,
        'order_count': Order.objects.filter(user=request.user).count(),
        'recent_products': recent_products,
    }

    return render(
        request,
        'student/customer_dashboard.html',
        context
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@login_required(login_url='login')
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('customer_dashboard')

    today = timezone.localdate()
    seven_days_ago = today - timedelta(days=6)

    all_orders = Order.objects.exclude(status='Cancelled')

    total_revenue = all_orders.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_orders = Order.objects.count()

    total_products = product.objects.count()

    total_customers = User.objects.filter(
        is_staff=False,
        is_superuser=False
    ).count()

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    low_stock_products = product.objects.filter(
        stock__lte=5
    ).order_by('stock')[:6]

    recent_orders = Order.objects.select_related(
        'user'
    ).order_by('-created_at')[:8]

    sales_labels = []
    sales_values = []

    for i in range(7):
        day = seven_days_ago + timedelta(days=i)

        daily_sales = Order.objects.filter(
            created_at__date=day
        ).exclude(
            status='Cancelled'
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        sales_labels.append(day.strftime('%a'))
        sales_values.append(float(daily_sales))

    context = {
    'total_revenue': total_revenue,
    'total_orders': total_orders,
    'total_products': total_products,
    'total_customers': total_customers,
    'pending_orders': pending_orders,
    'low_stock_products': low_stock_products,
    'recent_orders': recent_orders,
    'sales_labels': sales_labels,
    'sales_values': sales_values,
}

    return render(
        request,
        'student/admin_dashboard.html',
        context
    )

def logout_page(request):

    if request.method == "POST":
        logout(request)

    return redirect('login')

def home(request):
    return render(request,'student/home.html')

def products(request):

    all_products = product.objects.all()

    return render(
        request,
        'student/products.html',
        {
            'products': all_products
        }
    )

def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'student/register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'student/register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'student/register.html')

def product_detail(request, id):
    selected_product = get_object_or_404(product, id=id)

    return render(request, 'student/product_detail.html', {
        'product': selected_product
    })