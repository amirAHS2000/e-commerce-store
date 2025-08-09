from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    # API endpoints
    path('api/cart/', views.cart_detail_api, name='cart-detail-api'),
    path('api/cart/add/', views.add_to_cart_api, name='add-to-cart-api'),
    path('api/cart/update/<int:item_id>/', views.update_cart_item_api, name='update-cart-item-api'),
    path('api/checkout/', views.checkout_api, name='checkout-api'),
    path('api/history/', views.order_history_api, name='order-history-api'),
]
