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

    # override save_formset to set the price for CartItems
    def save_formset(self, request, form, formset, change):
        # get the instances from the formset, but don't save to DB yet
        instances = formset.save(commit=False)
        for instance in instances:
            # check if it's a new CartItem being added and if a product is selected
            # and if the price hasn't been set yet (e.g., if re-editing an existing item)
            if isinstance(instance, CartItem) and instance.product and not instance.price:
                instance.price = instance.product.price

            instance.save()
        formset.save_m2m() # save ManyToMany relations if any (not relevant for CartItem, but good practice)
        super().save_formset(request, form, formset, change)


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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, OrderItem) and instance.product and not instance.price:
                instance.price = instance.product.price
            instance.save()
        formset.save_m2m()
        super().save_formset(request, form, formset, change)

    def save_related(self, request, form, formsets, change):
        # call the parent method first to ensure all inlines are saved
        super().save_related(request, form, formsets, change)

        # get the Order instance that was just saved
        order = form.instance
        # now, all OrderItems for this order are in the database, so calculate_total_price() will work.
        order.total_price = order.calculate_total_price()
        # Save only the total_price field to avoid re-triggering the full save logic (and potential recursion)
        order.save(update_fields=['total_price'])


admin.site.register(Order, OrderAdmin)
