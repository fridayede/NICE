from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from .models import Category,Product,Img



def home (request):
    categories = Category.objects.all()
    products =Product.objects.all()
    return render(request,'product/index.html',{"categories":categories,"products":products})


def  product_cate(request, cate_slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category,slug=cate_slug)
    products=Product.objects.filter(category=category)
    return render(request,'product/index.html',{"category":category,"products":products,"categories":categories })



def product_detail(request,product_id):
    product=get_object_or_404(Product, id=product_id)
    product_images = Img.objects.filter(product=product)
    categories = Category.objects.all()
    return render(request,'product/product.html',{"product":product,"product_images":product_images,"categories":categories})

