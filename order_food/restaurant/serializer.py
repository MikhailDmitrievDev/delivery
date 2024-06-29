from rest_framework import serializers
from .models import Restaurant, Dish, Order, ItemCart, OrderDish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'dishes']


class OrderSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'price', 'time', 'dishes']

    def get_dishes(self, obj):
        order_dishes = obj.orderdish_set.all()

        serialized_dishes = []

        for order_dish in order_dishes:
            dish_data = {
                'id': order_dish.dish.id,
                'name': order_dish.dish.name,
                'price': order_dish.dish.price,
                'quantity': order_dish.quantity
            }
            serialized_dishes.append(dish_data)

        return serialized_dishes
