from django.contrib import admin
from .models import HeroSliderProduct, ContactModel, NewsLetter
from shop.models import ProductModel, ProductStatusType # حتما این رو چک کن که در مدل شاپ باشه

@admin.register(HeroSliderProduct)
class HeroSliderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'is_active', 'created_date')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product__title',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """فیلتر کردن محصولات برای نمایش فقط محصولات منتشر شده در لیست انتخاب اسلایدر"""
        if db_field.name == "product":
            # فرض بر این است که در مدل ProductModel فیلد status وجود دارد
            kwargs["queryset"] = ProductModel.objects.filter(
                status=ProductStatusType.publish.value
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_seen', 'created_date')
    list_filter = ('is_seen', 'created_date')
    search_fields = ('full_name', 'email', 'content')
    readonly_fields = ('created_date', 'updated_date') # معمولا اینها نباید دستی تغییر کنند

@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    search_fields = ('email',)