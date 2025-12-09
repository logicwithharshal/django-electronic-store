from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Cart
from .forms import DeliveryForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.last() or Cart.objects.create()
    existing_item = cart.items.filter(product=product).first()
    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1)
        cart.items.add(cart_item)
    return redirect('view_cart')

def view_cart(request):
    cart = Cart.objects.last()
    total = 0
    if cart:
        total = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'store/cart.html', {'cart': cart, 'total': total})

def clear_cart(request):
    Cart.objects.all().delete()
    return redirect('view_cart')

def delivery_view(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            Cart.objects.all().delete()
            return redirect('thank_you')
    else:
        form = DeliveryForm()
    return render(request, 'store/delivery.html', {'form': form})

def thank_you(request):
    return render(request, 'store/thank_you.html')
