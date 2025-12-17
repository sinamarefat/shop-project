import requests


class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    def payment_request(self, amount: int, description="پرداختی کاربر"):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "callback_url": self._callback_url,
            "description": description,
        }

        response = requests.post(self._payment_request_url, json=payload)
        return response.json()

    def payment_verify(self, amount: int, authority: str):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority,
        }

        response = requests.post(self._payment_verify_url, json=payload)
        return response.json()

    def generate_payment_url(self, authority: str):
        return f"{self._payment_page_url}{authority}"


if __name__ == "__main__":
    zarinpal = ZarinPalSandbox(
        merchant_id="4ced0a1e-4ad8-4309-9668-3ea3ae8e8897"
    )

    print("=== Payment Request ===")
    response = zarinpal.payment_request(15000)
    print(response)

    if response.get("data") and response["data"].get("authority"):
        authority = response["data"]["authority"]

        input("\nproceed to generating payment url?")
        print(zarinpal.generate_payment_url(authority))

        input("\ncheck the payment?")
        verify_response = zarinpal.payment_verify(15000, authority)
        print(verify_response)
    else:
        print("\n❌ Payment request failed")
