from django.contrib import admin

from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'about', 'birth_day']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'img', 'is_sale']
    search_fields = ['id', 'title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'avatar']


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ['value']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'star', 'product']


@admin.register(CartContent)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'qty']


admin.site.site_title = 'Книжный магазин'
admin.site.site_header = 'Книжный магазин'
