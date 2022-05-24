from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя автора')
    birth_day = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    about = models.TextField(verbose_name='Об авторе')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(verbose_name='Описание')
    cat = models.ManyToManyField(Category, verbose_name='Категория')
    img = models.ImageField(upload_to='product/')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    is_sale = models.BooleanField(default=True, verbose_name='В продаже')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_det', kwargs={'product_slug': self.slug})

    def get_categories(self):
        return [cat.title for cat in self.cat.all()]

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        index_together = (('id', 'slug'),)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return 'Личный кабинет {}'.format(self.user.username)

    class Meta:
        verbose_name = 'Личный кабинет'
        verbose_name_plural = 'Личные кабинеты'


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Cart(models.Model):
    session_key = models.CharField(max_length=999, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_cost = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)

    def get_total(self):
        items = CartContent.objects.filter(cart=self.id)
        total = 0
        for item in items:
            total += item.product.price * item.qty
        return total

    def get_cart_content(self):
        cart_content = CartContent.objects.filter(cart=self.id)
        return cart_content


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=True)

# def clean_cart(self, response=None):
#     cart_content = self.product.filter()
#
#     if response:
#         response.set_cookie('cart_count', len(cart_content))
#         return response
