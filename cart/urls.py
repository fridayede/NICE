from django.urls import path
from . import views

app_name ='cart'

urlpatterns = [
    path('',views.add_cart,name='add_cart'),
    path('/cart/',views.cart_list, name='cart_list'),
    path('/remove/',views.remove_cart_item,name='remove'),
     path('/increase/', views.increase_quantity, name='increase'),
    path('/reduce/', views.reduce_quantity, name='reduce'),
    path('/order/', views.order, name='order'),
    
]