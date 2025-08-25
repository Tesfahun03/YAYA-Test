# YAYA Wallet Webhook Receiver

This Django project provides a secure webhook endpoint for receiving and verifying payment notifications from YaYa Wallet.

## Features
- Receives POST webhook events at a Django endpoint
- Verifies the presence and authenticity of the `YAYA-SIGNATURE` header
- Validates the request body against the expected JSON structure
- Concatenates payload values in the required order to form the signed payload
- Computes and compares HMAC SHA256 signatures using a signing secret
- Enforces a 5-minute timestamp tolerance to prevent replay attacks
- Returns a simple JSON response with the sender's name and amount

## Assumptions
- The webhook payload always contains the following fields in this order:
  - `id`, `amount`, `currency`, `created_at_time`, `timestamp`, `cause`, `full_name`, `account_name`, `invoice_url`
- The signing secret is provided as a string in the code (replace `YOUR_SIGNING_SECRET_HERE` in `views.py` with your actual secret)
- The server time is synchronized (for timestamp tolerance)
- Only requests from YaYa Wallet's documented IP addresses should be trusted (IP filtering is recommended in production)

## Technologies Used
- Python 3
- Django (web framework)
- Standard Python libraries: `json`, `hmac`, `hashlib`, `time`

## How to Use
1. Clone the repository and install dependencies (Django).
2. Set your YaYa Wallet signing secret in `Webhooks/views.py`:
   ```python
   YAYA_SIGNING_SECRET = "YOUR_SIGNING_SECRET_HERE"
   ```
3. Run Django migrations and start the server:
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```
4. Configure YaYa Wallet to send webhooks to your endpoint (e.g., `https://yourdomain.com/webhooks/payment_webhook/`).

## Security Notes
- Always keep your signing secret safe and never expose it publicly.
- Consider adding IP allow-listing for YaYa Wallet's official IPs.
- Adjust timestamp tolerance as needed for your use case.

## Example Webhook Payload
```
{
  "id": "1dd2854e-3a79-4548-ae36-97e4a18ebf81",
  "amount": 100,
  "currency": "ETB",
  "created_at_time": 1673381836,
  "timestamp": 1701272333,
  "cause": "Testing",
  "full_name": "Abebe Kebede",
  "account_name": "abebekebede1",
  "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
}
```


