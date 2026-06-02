import random
import string
from datetime import datetime, timezone
from flask import current_app
def generate_otp(length: int = 6) -> str:
    if current_app.config.get('OTP_DEMO_MODE', True):
        return current_app.config.get('OTP_DEMO_CODE', '123456')
    return ''.join(random.choices(string.digits, k=length))
def send_otp_sms(phone: str, otp: str) -> bool:
    if current_app.config.get('OTP_DEMO_MODE', True):
        print(
            f"\n{'='*60}\n"
            f"  [DEMO OTP] Phone: {phone}  ->  OTP: {otp}\n"
            f"  (In production this will be sent via SMS)\n"
            f"{'='*60}\n"
        )
        return True
    try:
        from twilio.rest import Client
        account_sid = current_app.config['TWILIO_ACCOUNT_SID']
        auth_token  = current_app.config['TWILIO_AUTH_TOKEN']
        from_number = current_app.config['TWILIO_FROM_NUMBER']
        if not all([account_sid, auth_token, from_number]):
            current_app.logger.warning('Twilio credentials are not configured.')
            return False
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=f"Your FASTag OTP is: {otp}. Valid for 5 minutes. Do not share.",
            from_=from_number,
            to=f'+91{phone}'
        )
        return True
    except Exception as exc:
        current_app.logger.error(f'OTP SMS send failed: {exc}')
        return False
