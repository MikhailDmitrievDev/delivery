from django.db import models

from user.models import Cart, User


class Restaurant(models.Model):
    """Модель ресторана"""
    name = models.CharField(max_length=255)


class Dish(models.Model):
    """Модель блюда"""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    restaurant = models.ForeignKey(Restaurant, related_name='dishes', on_delete=models.CASCADE)


class ItemCart(models.Model):
    """Модель связи продукта к корзине."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    dishes = models.ManyToManyField(Dish, through='OrderDish')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
