from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'created_at', 'updated_at', 'get_total_price')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username',)

    class CartItemInline(admin.TabularInline):
        model = CartItem
        extra = 1
        fields = ('product', 'quantity', 'price')
        readonly_fields = ('price',)

    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('total_price', 'created_at')

    class OrderItemInline(admin.TabularInline):
        model = OrderItem
        extra = 1
        fields = ('product', 'quantity', 'price')
        readonly_fields = ('price',)

    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
