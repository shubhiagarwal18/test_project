# from django.conf import settings
# from django.conf.urls import static
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    mrp = models.IntegerField(default=10000)
    image = models.ImageField(upload_to='', null=True, blank=True, default='default_pic.jpg')

    def __str__(self) -> str:
        return self.name
    # def image_path(self):
    #     return self.image.url[len(settings.MEDIA_URL):]

class Order(models.Model):
    product = models.ManyToManyField(Product)
    user = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user

class ReviewBase(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    def __str__(self) -> str:
        return self.text

class ProductReview(ReviewBase):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.user.username

