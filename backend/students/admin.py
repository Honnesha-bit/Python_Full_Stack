from django.contrib import admin

# Register your models here.
from .models import product

from django.contrib import admin

from .models import (
    students,
    product,
    CartItem,
    WishlistItem,
    Order,
    OrderItem
)


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('stock',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'payment_method',
        'status',
        'created_at'
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'id')


admin.site.register(students)
admin.site.register(CartItem)
admin.site.register(WishlistItem)
admin.site.register(OrderItem)
