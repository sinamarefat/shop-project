from django import template
from shop.models import ProductStatusType, ProductModel,WishlistProductModel

register = template.Library()



@register.inclusion_tag("includes/latest-products.html")
def show_latest_products():
    latest_products = ProductModel.objects.filter(
        status=ProductStatusType.publish.value
    ).distinct().order_by("-created_date")[:8]

    return {"latest_products": latest_products}


@register.inclusion_tag("includes/similar-products.html")
def show_similar_products(product):
    # request = context.get("request")
    product_categories= product.category.all()
    similar_prodcuts = ProductModel.objects.filter(
        status=ProductStatusType.publish.value,category__in=product_categories).order_by("-created_date")[:4]
    # wishlist_items =  WishlistProductModel.objects.filter(user=request.user).values_list("product__id",flat=True) if request.user.is_authenticated else []
    return {"similar_prodcuts": similar_prodcuts}


