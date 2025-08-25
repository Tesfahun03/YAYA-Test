
import json
import hmac
import hashlib
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Replace with your actual YaYa Wallet signing secret
YAYA_SIGNING_SECRET = "YOUR_SIGNING_SECRET_HERE"
# i put it here for simplisity should be in env variables


@csrf_exempt  # Exempt this view from CSRF protection
def payment_webhook(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    # Check for YAYA-SIGNATURE header
    signature = request.headers.get("YAYA-SIGNATURE")
    if not signature:
        return HttpResponseBadRequest("Missing YAYA-SIGNATURE header.")

    try:
        # Parse JSON body
        data = json.loads(request.body)

        # Prepare signed_payload by concatenating all values in order
        payload_order = [
            "id", "amount", "currency", "created_at_time", "timestamp", "cause", "full_name", "account_name", "invoice_url"
        ]
        try:
            signed_payload = "".join(str(data[k]) for k in payload_order)
        except KeyError:
            return HttpResponseBadRequest("Missing required fields in payload.")

        # Compute expected signature
        expected_signature = hmac.new(
            YAYA_SIGNING_SECRET.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        # Compare signatures (constant time)
        if not hmac.compare_digest(signature, expected_signature):
            return HttpResponseBadRequest("Invalid signature.")

        # Check timestamp tolerance (5 minutes) if signiture is valid
        try:
            event_timestamp = int(data["timestamp"])
        except (KeyError, ValueError):
            return HttpResponseBadRequest("Invalid or missing timestamp.")

        import time
        current_timestamp = int(time.time())
        if abs(current_timestamp - event_timestamp) > 300:
            return HttpResponseBadRequest("Timestamp outside allowed tolerance.")

        # Extract simple fields from webhook body
        full_name = data.get("full_name")
        amount = data.get("amount")
        # Do something simple: return a message with the name and amount
        return JsonResponse({"message": f"Received payment from {full_name} of amount {amount}"}, status=200)

        # performing own logic from the incoming webhook
        # Process_webhook()

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")
