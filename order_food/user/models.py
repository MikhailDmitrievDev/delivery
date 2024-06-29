from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель кастомного пользователя."""
    wallet = models.DecimalField(max_digits=10, decimal_places=1, default=0)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)

        if created:
            Cart.objects.create(user=self)


class Cart(models.Model):
    """Модель корзины пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
