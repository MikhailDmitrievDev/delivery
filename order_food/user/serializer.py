from rest_framework import serializers

from restaurant.models import ItemCart
from user.models import User, Cart


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class CartItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.ReadOnlyField(source='dish.name')
    price = serializers.SerializerMethodField()

    class Meta:
        model = ItemCart
        fields = ['id', 'dish', 'dish_name', 'price', 'quantity']

    def get_price(self, obj):
        return obj.dish.price * obj.quantity


class AddToCartSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
