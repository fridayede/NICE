from django.shortcuts import render, redirect
from django.http import JsonResponse
from product.models import Product
from .models import Cart,CartItem,Order,OrderItem
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_cart(request):
    if request.user.is_authenticated:
        print("login")
        print("trying to buy")
        product_id = request.POST.get("product-id")
        if not product_id:
            return JsonResponse({"success": False, "error": "No product id provided"})
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product does not exist"})
        cart = None
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        cart_item = None
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
            print("cart_item.quantity", cart_item.quantity)
            print("cart item exist")
        except CartItem.DoesNotExist:
            print("created cart item")
            cart_item = CartItem.objects.create(cart=cart, product=product)

        print("product-id", product_id)
    
     
        
    return JsonResponse({"success":True})
    return redirect(request,"index.html")






def cart_list(request):
    cart =Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    for cart_item in cart_items:
        cart_item.total_price = cart_item.product.price * cart_item.quantity
        cart_item.save()
    return render(request, 'cart/index.html', {'cart_items': cart_items, 'total_price': total_price})





def remove_cart_item(request):
    print("cart remove")
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        cart_item_id = request.POST.get('item_id')
        if not cart_item_id:
            print("No item_id provided")
            return redirect('cart:cart_list')
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
            cart_item.delete()
        except (Cart.DoesNotExist, CartItem.DoesNotExist) as e:
            print(e)
    return redirect('cart:cart_list')
   
        
 
    
    
def increase_quantity(request):
    print("increase")
    if request.method == 'POST':
        cart_item_id = request.POST.get('item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart_list') 
        
        
def reduce_quantity(request):
    print("decrease")
    if request.method == 'POST':
        cart_item_id = request.POST.get('item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart:cart_list')
    
    
    
    

def order(request):
    print("trying to make an order")
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    order = Order.objects.create(user=request.user)
    total_price=0
    
    
    for cart_item in cart_items:
        OrderItem.objects.create(product=cart_item.product,order=order, quantity=cart_item.quantity,total_price=cart_item.total_price,paid =False,status="pending")
        total_price += cart_item.total_price
        pass
        print(cart_item.total_price)

        
        
    order.total_price =total_price
    print(f"Total price for order: {order.total_price}")
    order.save()
    order.delete()

    return render(request,"order/index.html",{'order':order})

