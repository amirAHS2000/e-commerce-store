from .models import Cart, CartItem, OrderItem, Order
from products.models import Product 
from .forms import OrderForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.db import IntegrityError, transaction


def _get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, is_active=True)
    return cart

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = _get_or_create_cart(request.user)

    # get quantity from POST data, default to 1 if not present or invalid
    quantity_str = request.POST.get('quantity', '1')
    try:
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    
    # check if the product is already in the cart
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.quantity += quantity
        messages.success(request, f'Updated quantity for {product.name}!')
    else:
        # create a new cart item
        try:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                price=product.price
            )
            messages.success(request, f'Added {product.name} to cart!')
        except IntegrityError:
            # handle potential race conditions where another process adds the same item
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            if cart_item:
                cart_item.quantity += quantity
                messages.success(request, f'Updated quantity for {product.name}!')
    
    cart_item.save()
    return redirect('orders:view_cart')

@login_required
def view_cart(request):
    cart = _get_or_create_cart(request.user)
    context = {
        'cart': cart
    }
    return render(request, 'orders/cart_detail.html', context)

@login_required
@require_POST
def update_cart_item(request, item_id):
    # ensure the cart item belongs to the user's active cart
    cart = _get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    # get the quantity from POST data
    quantity_str = request.POST.get('quantity')
    if quantity_str is not None:
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                cart_item.delete()
                messages.warning(request, 'Item removed from cart.')
            else:
                # update to the specific quantity, not increment
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart item updated successfully!')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity provided.')
    else:
        messages.error(request, 'Quantity not provided.')
    
    return redirect('orders:view_cart')

@login_required
def checkout(request):
    cart = _get_or_create_cart(request.user)

    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('orders:view_cart')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # create the Order object
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = cart.get_total_price()
                order.status = 'PENDING'
                order.save()

                # create OrderItems from CartItems
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.price
                    )

                    # update Inventory
                    # TODO

                # deactivate the cart
                cart.is_active = False
                cart.save()

            messages.success(request, 'Your order has been placed!')
            return redirect('orders:order_confirmation', order_id=order.id)        
    else: # GET request
        form = OrderForm()

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    # fetch the order, ensuring it belongs to the logged-in user
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'orders/order_confirmation.html', context)
