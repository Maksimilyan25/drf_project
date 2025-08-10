from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Кастомная модель Юзера."""

    full_name = models.CharField(max_length=100, verbose_name='Полное имя')
    age = models.PositiveIntegerField(verbose_name='Возраст', validators=[
        MinValueValidator(1), MaxValueValidator(100)
    ])
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'age']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name


class Order(models.Model):
    """Модель заказов."""

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=500, verbose_name='Описание')
    user = models.ForeignKey(
        'User', related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name
