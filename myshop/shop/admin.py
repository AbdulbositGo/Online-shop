from django.contrib import admin

from .models import Category, Product


@admin.registry(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_dislplay = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'crated', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
