from django.contrib import admin
from .models import (
    Category, Product, ProductImage,
    ProductAttribute, ProductPrice,
    ProductComment, ProductRating
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'alt_text')
    search_fields = ('alt_text',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'key', 'value')
    list_filter = ('key',)
    search_fields = ('key', 'value')


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'current_price', 'old_price', 'currency')
    list_filter = ('currency',)
    search_fields = ('product__name',)


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'created_at')
    search_fields = ('name', 'comment')
    date_hierarchy = 'created_at'


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'
