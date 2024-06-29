from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restaurant.models import ItemCart, Dish
from user.models import User, Cart
from user.serializer import UserSerializer, CartItemSerializer, AddToCartSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        user = request.user
        serializer_user = UserSerializer(user, context={'request': request})
        return Response(serializer_user.data, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        user_cart = Cart.objects.get(user=user_id)
        cart_items = ItemCart.objects.filter(cart=user_cart)
        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        data = {
            'total_price': sum(item.get('price', 0) for item in cart_items_serializer.data),
            'positions': cart_items_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        user_id = request.user.id
        user_cart = Cart.objects.get(user=user_id)

        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            dish_id = serializer.validated_data.get('dish_id')
            quantity = serializer.validated_data.get('quantity')

            try:
                dish = Dish.objects.get(id=dish_id)
                item, created = ItemCart.objects.get_or_create(cart=user_cart, dish=dish)
                item.quantity = quantity
                item.save()
                return Response(
                    {'message': f'Добавили блюдо с id: {dish_id} добавили в корзину, кол-во: {quantity}'},
                    status=status.HTTP_200_OK)
            except Dish.DoesNotExist:
                return Response({'error': 'Блюдо не найдено'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='delete')
    def delete_item(self, request):
        user_id = request.user.id
        dish_id = request.data.get('dish_id')
        quantity = request.data.get('quantity')

        user_cart = Cart.objects.get(user=user_id)
        try:
            cart_item = ItemCart.objects.get(dish_id=user_cart.id, cart_id=dish_id)
            remains = cart_item.quantity - quantity
            if remains <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = remains
                cart_item.save()
            return Response({'detail': f'Убрали блюдо из корзины'},
                            status=status.HTTP_200_OK)
        except ItemCart.DoesNotExist:
            return Response({'detail': "Нет такого блюда в корзине."})
