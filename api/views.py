from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from users.models import Order, User
from .serialzers import (
    CreateUserSerializer,
    CreateOrderSerializer,
    DetailUserSerializer,
    OrderSerializer
)
from .permissions import AuthorOnlyPermission


@extend_schema(tags=['Пользователи'])
class UserView(ModelViewSet):
    """Вьюсет для пользователей."""

    queryset = User.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):

        if self.action == 'create' or self.request.method == 'POST':
            return CreateUserSerializer
        return DetailUserSerializer

    def get_permissions(self):
        if self.action == 'create' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


@extend_schema(tags=['Заказы'])
class OrderView(ModelViewSet):
    """Вьюсет для заказов."""

    permission_classes = (AuthorOnlyPermission,)
    queryset = Order.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        """Автоназначение пользователя при создании заказа."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Автообновление пользователя при изменении заказа."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.request.method == 'POST':
            return CreateOrderSerializer
        else:
            return OrderSerializer
