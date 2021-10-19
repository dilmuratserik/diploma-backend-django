from django.contrib import admin
from .models import Product, ProductImage
from django import forms

class PIAdmin(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category', )
    inlines = [PIAdmin]
    search_fields = ('name', 'description')
    # exclude = ['count_rec', 'sale_price']

admin.site.register(Product, ProductAdmin)
