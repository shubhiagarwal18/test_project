from django.contrib import admin
from test_app.models import *

# Register your models here.

class ProductList(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

class OrdersList(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    
class CategoryList(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]


admin.site.register(Product, ProductList)
admin.site.register(Category, CategoryList)
admin.site.register(Order, OrdersList)
admin.site.register(ProductReview)
admin.site.register(UserProfile)

  