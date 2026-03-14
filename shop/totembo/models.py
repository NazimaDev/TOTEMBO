from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг категории')
    icon = models.ImageField(upload_to='icon/', verbose_name='Иконка', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родитель',
                               related_name='subcategories', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    slug = models.SlugField(unique=True, verbose_name='Слаг товара')
    desc = models.TextField(verbose_name='Описание товара')
    price = models.IntegerField(verbose_name='Цена товара в Сумах')
    quantity = models.IntegerField(verbose_name='Кол-во товара', default=15)
    color_name = models.CharField(max_length=50, verbose_name='Название цвета')
    discount = models.IntegerField(default=0, verbose_name='Скидка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='products')
    model = models.ForeignKey('ModelProduct', on_delete=models.CASCADE, verbose_name='Модель товара')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except Exception:
                return ''
        else:
            return ''

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ModelProduct(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название модели')
    slug = models.SlugField(unique=True, verbose_name='Слаг модели')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели товаров'


class ImagesProduct(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар',
                                related_name='images')

    def __str__(self):
        return f'Фото товара {self.product.title}'

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=25, verbose_name='Номер телефона')
    region = models.CharField(max_length=50, verbose_name='Регион', null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name='Город', null=True, blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', null=True, blank=True)
    home = models.CharField(max_length=50, verbose_name='Дом №', null=True, blank=True)
    flat = models.CharField(max_length=50, verbose_name='Квартира №', null=True, blank=True)

    def __str__(self):
        return f'Покупатель {self.user.username}'

    class Meta:
        verbose_name = 'Покупателя'
        verbose_name_plural = 'Покупатели'


class EmailSubscription(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписку на email'
        verbose_name_plural = 'Подписки на email'


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PAID = 'paid'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_CANCELED, 'Отменён'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Покупатель',
    )
    first_name = models.CharField(max_length=250, verbose_name='Имя')
    last_name = models.CharField(max_length=250, verbose_name='Фамилия')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    city = models.CharField(max_length=100, verbose_name='Город')
    region = models.CharField(max_length=300, verbose_name='Регион')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    total_price = models.IntegerField(verbose_name='Сумма заказа в Сумах')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name='Статус заказа',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Заказ #{self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.IntegerField(verbose_name='Цена за единицу на момент заказа')

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'








