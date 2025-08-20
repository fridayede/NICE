from django.db import models



# Create your models here
class Category(models.Model):
    name =models.CharField(max_length=225)
    slug = models.SlugField(unique=True) 
    # unique=True
    
    
    def __str__(self):
        return self.name
    
    
    
class Product(models.Model):
    category =models.ForeignKey(Category,related_name="products", on_delete=models.CASCADE)
    name =models.CharField(max_length=225)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    created =models.DateField(auto_now_add=True)
    productimage = models.ImageField(upload_to="products/")
    rating =models.IntegerField()
    summary = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    
    
    def __str__(self):
        return self.name
    
    
    
class Img(models.Model):
    product = models.ForeignKey(Product,related_name="images",on_delete=models.CASCADE)
    productimage =models.ImageField(upload_to="products/")
    
    
    def __str__(self):
        return self.product.name



