
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator, RegexValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d',
        default='images/avatars/default.jpg',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='URL категории', max_length=255, blank=True, unique=True)
    description = models.TextField(verbose_name='Описание категории')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = TreeForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    thumbnail = models.ImageField(default='default.jpg',
                                  verbose_name='Изображение товара',
                                  blank=True,
                                  upload_to='images/products/%Y/%m/%d/',
                                  validators=[
                                      FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product)
    session_key = models.CharField(max_length=32, null=True, blank=True, unique=True)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)


class OrderItem(models.Model):
    user = models.ForeignKey(User, related_name='order_items', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=255)
    review_date = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    value = models.BigIntegerField(default=True, verbose_name='Значение')
    created_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()


class Requisites(models.Model):
    user = models.ForeignKey(User, related_name='requisites', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])


class Delivery(models.Model):
    user = models.ForeignKey(User, related_name='deliveries', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    requisite = models.ForeignKey(Requisites, related_name='payments', on_delete=models.CASCADE)
    address = models.ForeignKey(Delivery, related_name='payments', on_delete=models.CASCADE)
