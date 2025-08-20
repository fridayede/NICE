from django.urls import path
from . import views



app_name ="product"
urlpatterns = [
    path('',views.home, name="home"),
    path('<slug:cate_slug>/',views.product_cate,name="product_cate"),
    path('details/<int:product_id>/',views.product_detail, name="product_detail")
]
