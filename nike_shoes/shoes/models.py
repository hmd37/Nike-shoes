from django.db import models
from django.contrib.auth.models import User


class Info(models.Model):
    star = models.FloatField()
    num_of_comments = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=1024)

class Shoe(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=32)
    price = models.PositiveIntegerField()
    num_of_colors = models.PositiveSmallIntegerField()
    size = models.FloatField()
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shoe_images/', blank=True, null=True)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)