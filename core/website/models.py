from django.db import models
from shop.models import ProductModel

# Create your models here.

class HeroSliderProduct(models.Model):
    """مدل برای مدیریت محصولات نمایش داده شده در Hero Slider صفحه اصلی"""
    product = models.ForeignKey(
        ProductModel, 
        on_delete=models.CASCADE,
        verbose_name="محصول",
        related_name="hero_sliders"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
        help_text="عدد کوچکتر اول نمایش داده می‌شود"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_date']
        verbose_name = "محصول اسلایدر اصلی"
        verbose_name_plural = "محصولات اسلایدر اصلی"
        
    def __str__(self):
        return f"{self.product.title} - ترتیب: {self.order}"
