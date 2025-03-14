
import random
from django.utils import timezone
from datetime import datetime, timedelta
import Tshirts.settings as settings
from django.contrib.auth import get_user_model
from twilio.rest import Client



def get_otp():
    otp=str(random.randint(1000,9999))
    return otp

User=get_user_model()
def generate_otp(user: User):
    otp=get_otp()
    user.otp=otp
    user.otp_expiry= timezone.now() + timedelta(days=1)
    user.save()
    return

def send_otp(user: User):
    phone=user.phone
    if (not (user.max_otp_try is None)) and user.max_otp_try==0:
        if not user.otp_max_out<timezone.now():
            raise Exception("max_otp_try is 0, try again after 10 minutes")
        user.max_otp_try=5
        user.save()
    generate_otp(user)
    #todo send link otp
    account_sid = settings.TWILO_ACCOUNT_SID
    auth_token = settings.TWILO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='+12723463013',
    body = f'your otp is {user.otp}',
    to = f'+91{phone}'
    )
    print(message.sid)
    user.max_otp_try=user.max_otp_try-1
    print(user.max_otp_try)
    if user.max_otp_try==0:
        user.otp_max_out=datetime.now()+timedelta(minutes=10)
    user.save()
    return


from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'name': user.name,
        'phone': user.phone,
    }