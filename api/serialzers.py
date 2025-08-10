from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User, Order


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all())
    ])

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'age', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
            'full_name': {'required': True},
        }

    def create(self, validated_data):
        """Переопределяем метод для безопасного создания пользователя."""
        user = User.objects.create_user(
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            **validated_data
        )
        return user


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'age')


class CreateOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа."""

    class Meta:
        model = Order
        fields = ('id', 'name', 'description', 'user')
        read_only_fields = ('user',)

    def validate_user(self, value):
        try:
            return User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с таким ID не существует')


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов."""

    class Meta:
        model = Order
        fields = ('id', 'name', 'description', 'user')
