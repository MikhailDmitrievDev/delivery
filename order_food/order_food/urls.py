"""
URL configuration for order_food project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from restaurant.views import MenuView, OrderView
from user.views import UserViewSet, CartViewSet

router = SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'menu', MenuView, basename='menu')
router.register(r'order', OrderView, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
