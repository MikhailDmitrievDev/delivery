"""View for Menu endpoint"""
from django.db import transaction
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restaurant.models import Restaurant, Order, ItemCart, OrderDish, Dish
from restaurant.serializer import RestaurantSerializer, OrderSerializer


class MenuView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'id']
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        filters = {
            'id': request.query_params.get('id'),
            'name__icontains': request.query_params.get('name')
        }

        query_params = {key: value for key, value in filters.items() if value is not None}
        filter_kwargs = {key: value for key, value in query_params.items()}

        queryset = queryset.filter(**filter_kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrderView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = Order.objects.filter(user_id=request.user.id)
        orders = OrderSerializer(query, many=True).data
        return_data = {
            'total_count': len(orders),
            'total_sum': sum(float(price.get('price')) for price in orders),
            'last_orders': orders

        }

        return Response(return_data)

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        user = request.user
        cart_items = ItemCart.objects.filter(cart_id=user.cart.id)
        if not cart_items:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                order = Order.objects.create(user=user, total_amount=0)
                for item in cart_items:
                    OrderDish.objects.create(order=order, dish=item.dish, quantity=item.quantity)
                    dish = Dish.objects.get(id=item.dish_id)
                    order.total_amount += dish.price * item.quantity
                if user.wallet < order.total_amount:
                    return Response({'detail': 'Недостаточно средст на счете'}, status=status.HTTP_400_BAD_REQUEST)
                user.wallet = user.wallet - order.total_amount
                user.save()
                cart_items.delete()
                order.save()
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"error": "Ошибка, транзакция не выполнена."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
