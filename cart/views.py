from django.shortcuts import render, redirect,get_object_or_404
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
            # cart = Cart.objects.get(user=request.user)
            cart = Cart.objects.filter(user=request.user).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)

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
    cart = Cart.objects.filter(user=request.user).first()
    # cart =Cart.objects.get(user=request.user)
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        cart = Cart.objects.create(user=request.user)
        print("cart", cart)
        cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if not cart:
        return render(request, 'index.html', {'message': 'Your cart is empty.'})

    for cart_item in cart_items:
        cart_item.total_price = cart_item.product.price * cart_item.quantity
        cart_item.save()

    return render(request, 'cart/index.html', {'cart_items': cart_items, 'total_price': total_price})




def cart_list(request):
    # cart =Cart.objects.get(user=request.user)
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if total_price >= 0:
        print("No items in cart")
        # return redirect('cart:cart_list')
        return render(request, 'index.html', {'message': 'Your cart is empty.'})

        # return render(request, 'product/product/index.html', {'error': 'No items in cart'})
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
    
    
    
    
    
    
    
    
    
@login_required















# def order(request):
#     print("Trying to make an order")

#     # Try to fetch the cart safely
#     cart = Cart.objects.filter(user=request.user).first()
#     cart_items = CartItem.objects.filter(cart=cart)
#     order = Order.objects.create(user=request.user)
#     total_price=0
    
#     if not cart:
#         return render(request, 'cart/index.html', {'message': 'Your cart is empty.'})

#     # Create the order
#     # for cart_item in cart_items:
#     for cart_item in cart_items:
#         OrderItem.objects.create(
#             product=cart_item.product,
#             order=order,
#             quantity=cart_item.quantity,
#             total_price=cart_item.total_price,
#             paid=False,
#             status="pending"
#     )

#     total_price += cart_item.total_price
#     pass
#     print(cart_item.total_price)
#     order = Order.objects.create(
#         user=request.user,
#         # total=cart.get_total(),  # make sure this method exists
#         # status='confirmed'
#     )

#     # Optionally move items from cart to order, if you track products in orders
#     for item in cart.items.all():
#         order.items.create(
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.price
#         )
#     order.total_price = total_price
#     print(f"Total price for order: {order.total_price}")

#     # ✅ Delete the cart
#     cart.delete()

#     # 🧾 Return confirmation page, no redirect
#     return render(request, 'order/index.html', {
#         'order': order
#     })
    
    
    

# def order(request):
#     print("trying to make an order")
#     cart = Cart.objects.get(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     order = Order.objects.create(user=request.user)
#     total_price=0
    
    
#     for cart_item in cart_items:
#         OrderItem.objects.create(product=cart_item.product,order=order, quantity=cart_item.quantity,total_price=cart_item.total_price,paid =False,status="pending")
#         total_price += cart_item.total_price
#         pass
#         print(cart_item.total_price)

        
        
#     order.total_price =total_price
#     print(f"Total price for order: {order.total_price}")
#     order.save()
    

#     return render(request,"order/index.html",{'order':order})






@login_required
# def order(request):
#     print("trying to make an order")
#     cart = Cart.objects.filter(user=request.user).first()

#     # cart = Cart.objects.get(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     order = Order.objects.create(user=request.user)
#     total_price=0
    
    
#     for cart_item in cart_items:
#         OrderItem.objects.create(product=cart_item.product,order=order, quantity=cart_item.quantity,total_price=cart_item.total_price,paid =False,status="pending")
#         total_price += cart_item.total_price
#         pass
#         print(cart_item.total_price)

        
        
#     order.total_price =total_price
#     print(f"Total price for order: {order.total_price}")
#     order.save()
#     order.delete()

#     return render(request,"order/index.html",{'order':order})







#   # Make sure Cart is imported



def order(request):

    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart:
        cart = Cart.objects.create(user=request.user)
    #   cart_items = CartItem.objects.filter(cart=cart)
    order = Order.objects.create(user=request.user, total_price=1)
    total_price = 0
    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity, total_price=cart_item.total_price, paid=False, status='pending')
        total_price += cart_item.total_price
        pass
    order.total_price = total_price
    if total_price == 0:
        print("No items in cart")
        # return redirect('cart:cart_list')
        return render(request, 'product/index.html', {'error': 'No items in cart'})
    order.save()
    return render(request, 'order/index.html', {'order': order, 'cart_items': cart_items, 'total_price': total_price})



def confirmation(request, confirmation_id):
    
    print("confirming order")

    if not confirmation_id:
        print("No order_id provided")
        return render(request, 'cart/cart_list.html', {'error': 'No order ID provided'})

    try:
        order = Order.objects.get(id=confirmation_id, user=request.user)
        # order.status = "confirmed"
        order.save()

        # ✅ Delete user's cart
        Cart.objects.filter(user=request.user).delete()
        print("Cart deleted.")

    except Order.DoesNotExist as e:
        print("Order not found:", e)
        return render(request, 'cart/cart_list.html', {'error': 'Order not found'})

    # ✅ Show confirmation page
    return render(request, 'order/confirmation.html', {'order': order})
