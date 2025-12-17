from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType

class PaymentVerifyView(View):
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status") # این پارامتر در کوئری استرینگ URL بازگشتی همچنان Status است

        payment_obj = get_object_or_404(
            PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        zarin_pal = ZarinPalSandbox()
        
        response = zarin_pal.payment_verify(
            int(payment_obj.amount), payment_obj.authority_id)
        
        # اصلاح شده: استخراج اطلاعات از ساختار data در نسخه 4
        # مثال پاسخ موفق: {'data': {'code': 100, 'message': '...', 'ref_id': 1234}, 'errors': []}
        
        ref_id = None
        status_code = 0
        
        if 'data' in response and response['data']:
            data = response['data']
            ref_id = data.get("ref_id")
            status_code = data.get("code")
        elif 'errors' in response:
             # اگر خطایی باشد، معمولا کد خطا در بخش errors است
             # اما برای سادگی فعلا 0 در نظر میگیریم که یعنی ناموفق
             status_code = 0 

        payment_obj.ref_id = ref_id
        payment_obj.response_code = status_code
        # کدهای 100 و 101 در زرین‌پال به معنی موفقیت است
        is_success = status_code in {100, 101}
        
        payment_obj.status = PaymentStatusType.success.value if is_success else PaymentStatusType.failed.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatusType.success.value if is_success else OrderStatusType.failed.value
        order.save()

        return redirect(reverse_lazy("order:completed") if is_success else reverse_lazy("order:failed"))