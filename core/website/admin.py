from django.contrib import admin
from .models import HeroSliderProduct

# Register your models here.

@admin.register(HeroSliderProduct)
class HeroSliderProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'is_active', 'created_date']
    list_filter = ['is_active', 'created_date']
    search_fields = ['product__title']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_date']
