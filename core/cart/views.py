
from typing import Any
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from shop.models import ProductModel, ProductStatusType
from .cart import CartSession


class SessionAddProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        
        if product_id:
            try:
                product = ProductModel.objects.get(id=product_id, status=ProductStatusType.publish.value)
                # Check stock availability
                current_quantity = cart.get_product_quantity(product_id)
                total_requested = current_quantity + quantity
                
                if total_requested > product.stock:
                    return JsonResponse({
                        "error": "موجودی کافی نیست",
                        "available_stock": product.stock,
                        "cart": cart.get_cart_dict(), 
                        "total_quantity": cart.get_total_quantity()
                    }, status=400)
                
                cart.add_product(product_id, quantity)
                if request.user.is_authenticated:
                    cart.merge_session_cart_in_db(request.user)
                return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})
            except ProductModel.DoesNotExist:
                return JsonResponse({"error": "محصول یافت نشد"}, status=404)
        
        return JsonResponse({"error": "خطا در افزودن محصول"}, status=400)


class SessionRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        if product_id:
            cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionUpdateProductQuantityView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        
        if product_id:
            try:
                product = ProductModel.objects.get(id=product_id, status=ProductStatusType.publish.value)
                if quantity > product.stock:
                    return JsonResponse({
                        "error": "موجودی کافی نیست",
                        "available_stock": product.stock,
                        "cart": cart.get_cart_dict(), 
                        "total_quantity": cart.get_total_quantity()
                    }, status=400)
                
                cart.update_product_quantity(product_id, quantity)
                if request.user.is_authenticated:
                    cart.merge_session_cart_in_db(request.user)
                return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})
            except ProductModel.DoesNotExist:
                return JsonResponse({"error": "محصول یافت نشد"}, status=404)
        
        return JsonResponse({"error": "خطا در به‌روزرسانی محصول"}, status=400)


class CartSummaryView(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context
