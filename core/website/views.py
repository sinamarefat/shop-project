from django.shortcuts import render

from django.views.generic import TemplateView
from shop.models import ProductModel, ProductStatusType
from .models import HeroSliderProduct


class IndexView(TemplateView):
    template_name = "website/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the last 3 products created
        context['latest_products'] = ProductModel.objects.filter(
            status=ProductStatusType.publish.value
        ).order_by('-created_date')[:3]
        
        # Get hero slider products
        context['hero_slider_products'] = HeroSliderProduct.objects.filter(
            is_active=True,
            product__status=ProductStatusType.publish.value
        ).select_related('product')
        
        return context


class ContactView(TemplateView):
    template_name = "website/contact.html" 


class AboutView(TemplateView):
    template_name = "website/about.html" 
