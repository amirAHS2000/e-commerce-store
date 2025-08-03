from django.contrib import admin
from .models import Category, Product, ProductImage, Inventory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    class ProductImageInline(admin.TabularInline):
        model = ProductImage
        extra = 1
        fields = ('image', 'alt_text', 'is_featured')

    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock_quantity', 'updated_at')
    search_fields = ('product__name',)

admin.site.register(Inventory, InventoryAdmin)
