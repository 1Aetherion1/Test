from django.conf import settings
from django.db import models


class Order(models.Model):
    def total_price(self):
        return sum(
            item.product_price()
            for item in self.orderitem_set.all()
        )
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, verbose_name='Пользователь')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(blank=True, null=True, verbose_name='Адрес доставке')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получение')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обработке', verbose_name='Статус заказа')


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказы')
    product = models.ForeignKey('goods.Products', on_delete=models.SET_DEFAULT, default=None, null=True, verbose_name='Продукт')
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    create_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')
    def product_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Проданные товар'
        verbose_name_plural = 'Проданные товары'
        db_table = 'order_item'
