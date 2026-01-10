import requests
import json
import base64
from datetime import datetime
from django.conf import settings
from .models import Payment


class MpesaAPI:
    """M-Pesa Daraja API integration class"""

    def __init__(self):
        self.config = settings.MPESA_CONFIG
        self.access_token = None

    def get_access_token(self):
        """Get OAuth access token from M-Pesa"""
        try:
            consumer_key = self.config["CONSUMER_KEY"]
            consumer_secret = self.config["CONSUMER_SECRET"]

            # Encode credentials
            credentials = base64.b64encode(
                f"{consumer_key}:{consumer_secret}".encode()
            ).decode()

            headers = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/json",
            }

            response = requests.get(self.config["ACCESS_TOKEN_URL"], headers=headers)
            response.raise_for_status()

            result = response.json()
            self.access_token = result["access_token"]
            return self.access_token

        except requests.RequestException as e:
            print(f"Error getting access token: {e}")
            return None

    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        """Initiate STK Push payment request"""
        if not self.access_token:
            self.get_access_token()

        if not self.access_token:
            return {"error": "Failed to get access token"}

        # Format phone number (remove + and ensure it starts with 254)
        phone_number = phone_number.lstrip("+")
        if not phone_number.startswith("254"):
            phone_number = (
                "254" + phone_number[1:]
                if phone_number.startswith("0")
                else phone_number
            )

        # Generate timestamp and password
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{self.config['BUSINESS_SHORTCODE']}{self.config['PASSKEY']}{timestamp}".encode()
        ).decode()

        payload = {
            "BusinessShortCode": self.config["BUSINESS_SHORTCODE"],
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": self.config["BUSINESS_SHORTCODE"],
            "PhoneNumber": phone_number,
            "CallBackURL": self.config["CALLBACK_URL"],
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc,
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                self.config["STK_PUSH_URL"], json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"STK Push error: {e}")
            return {"error": str(e)}

    def query_stk_status(self, checkout_request_id):
        """Query STK push payment status"""
        if not self.access_token:
            self.get_access_token()

        if not self.access_token:
            return {"error": "Failed to get access token"}

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{self.config['BUSINESS_SHORTCODE']}{self.config['PASSKEY']}{timestamp}".encode()
        ).decode()

        payload = {
            "BusinessShortCode": self.config["BUSINESS_SHORTCODE"],
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id,
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                self.config["STK_QUERY_URL"], json=payload, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"STK Query error: {e}")
            return {"error": str(e)}


def process_mpesa_callback(callback_data):
    """Process M-Pesa callback data and update payment status"""
    try:
        # Extract callback data
        stk_callback = callback_data.get("Body", {}).get("stkCallback", {})

        if stk_callback.get("ResultCode") == 0:
            # Payment successful
            callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

            # Extract relevant data
            mpesa_receipt_number = None
            transaction_date = None
            phone_number = None

            for item in callback_metadata:
                if item.get("Name") == "MpesaReceiptNumber":
                    mpesa_receipt_number = item.get("Value")
                elif item.get("Name") == "TransactionDate":
                    # Convert timestamp to datetime
                    transaction_date = datetime.strptime(
                        str(item.get("Value")), "%Y%m%d%H%M%S"
                    )
                elif item.get("Name") == "PhoneNumber":
                    phone_number = str(item.get("Value"))

            # Find and update payment
            merchant_request_id = stk_callback.get("MerchantRequestID")
            checkout_request_id = stk_callback.get("CheckoutRequestID")

            try:
                payment = Payment.objects.get(
                    merchant_request_id=merchant_request_id,
                    checkout_request_id=checkout_request_id,
                )

                payment.status = "completed"
                payment.mpesa_receipt_number = mpesa_receipt_number
                payment.transaction_date = transaction_date
                payment.phone_number = phone_number
                payment.save()

                # Activate subscription
                subscription = payment.subscription
                subscription.status = "active"
                subscription.save()

                return {
                    "status": "success",
                    "message": "Payment processed successfully",
                }

            except Payment.DoesNotExist:
                return {"status": "error", "message": "Payment not found"}

        else:
            # Payment failed
            result_desc = stk_callback.get("ResultDesc", "Unknown error")
            merchant_request_id = stk_callback.get("MerchantRequestID")
            checkout_request_id = stk_callback.get("CheckoutRequestID")

            try:
                payment = Payment.objects.get(
                    merchant_request_id=merchant_request_id,
                    checkout_request_id=checkout_request_id,
                )
                payment.status = "failed"
                payment.save()

                return {"status": "failed", "message": result_desc}

            except Payment.DoesNotExist:
                return {"status": "error", "message": "Payment not found"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
