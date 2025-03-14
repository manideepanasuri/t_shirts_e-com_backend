
from datetime import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers import *
User=get_user_model()
# Create your views here.

@api_view(['POST'])
def create_user_view(request):
    phone=request.data.get('phone')
    password=request.data.get('password')
    name=request.data.get('name')
    if phone is None or password is None or name is None:
        data={
            'success': False,
            'message':'Invalid data',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE);
    if len(phone)!=10:
        data={
            'success': False,
            'message': 'Phone number must be 10 digits',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    if User.objects.filter(phone=phone).exists():
        user=User.objects.get(phone=phone)
        data = {
            'success': False,
            'message': 'Phone number already exists please login',
        }
        if not user.is_verified:
            data={
                'success': False,
                'message': 'Please verify your phone number',
            }
        return Response(data,status=status.HTTP_405_METHOD_NOT_ALLOWED);
    try:
        user=User.objects.create_user(phone=phone,password=password,name=name,otp=get_otp(),otp_expiry=datetime.now()+timedelta(days=1))
    except Exception as e:
        data={
            'success': False,
            'message': str(e),
        }
        return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    data={
        'success': True,
        'message': 'success',
    }
    return Response(data,status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    phone=request.data.get('phone')
    password=request.data.get('password')
    if phone is None or password is None: return Response(data="Invalid data",status=status.HTTP_406_NOT_ACCEPTABLE)
    if len(phone)!=10:return Response(data="Invalid Phone number",status=status.HTTP_406_NOT_ACCEPTABLE)
    if not User.objects.filter(phone=phone).exists():return Response(data="User does not exists",status=status.HTTP_405_METHOD_NOT_ALLOWED)
    user=User.objects.get(phone=phone)
    if not user.check_password(password):
        data={
            'success': False,
            'message': 'Invalid password',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    if not user.is_verified:
        data={
            'success': False,
            'message': 'User verification failed',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    data={
        'success': True,
        'message': 'User login successfully',
        'data': get_tokens_for_user(user)
    }
    return Response(data,status=status.HTTP_200_OK)

@api_view(['POST'])
def verification_view(request):
    phone=request.data.get('phone')
    otp=request.data.get('otp')
    if phone is None or otp is None:
        data={
            'success': False,
            'message': 'Invalid data',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    if not User.objects.filter(phone=phone).exists():
        data={
            'success': False,
            'message': 'User does not exists',
        }
        return Response(data,status=status.HTTP_405_METHOD_NOT_ALLOWED)
    user=User.objects.get(phone=phone)
    if user.otp_expiry is None or timezone.now()>user.otp_expiry:
        data={
            'success': False,
            'message': 'OTP expired',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    if not user.otp==otp:
        data={
            'success': False,
            'message': 'Incorrect OTP',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    user.is_verified=True
    user.save()
    token=get_tokens_for_user(user)
    data={
        'success': True,
        'message': 'User verification successfully',
        'data': token
    }
    return Response(data,status=status.HTTP_200_OK)

@api_view(['POST'])
def sendOtp(request):
    phone=request.data.get('phone')
    print(phone)
    if phone is None:
        data={
            'success': False,
            'message': 'Invalid data',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    if not User.objects.all().filter(phone=phone).exists():
        data={
            'success': False,
            'message': 'User does not exists',
        }
        return Response(data,status=status.HTTP_405_METHOD_NOT_ALLOWED)
    user=User.objects.get(phone=phone)
    try:
        send_otp(user)
        data={
            'success': True,
            'message': 'OTP sent successfully',
        }
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        data={
            'success': False,
            'message': str(e),
        }
        print(e)
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def login_using_otp(request):
    phone=request.data.get('phone')
    if phone is None:
        return Response(data="Invalid data",status=status.HTTP_406_NOT_ACCEPTABLE)
    if not User.objects.filter(phone=phone).exists():
        return Response(data="User does not exists",status=status.HTTP_405_METHOD_NOT_ALLOWED)
    user=User.objects.get(phone=phone)
    try:
        send_otp(user)
    except Exception as e:
        print(e)
        return  Response(data="Error sending OTP try after 10 minitues",status=status.HTTP_429_TOO_MANY_REQUESTS)
    return Response(data="OTP sent Successfully",status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset_view(request):
    phone=request.data.get('phone')
    if phone is None:
        data={
            'success': False,
            'message': 'Invalid data',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    if not User.objects.filter(phone=phone).exists():
        data={
            'success': False,
            'message': 'User does not exists',
        }
        return Response(data,status=status.HTTP_405_METHOD_NOT_ALLOWED)
    user=User.objects.get(phone=phone)
    otp=request.data.get('otp')
    password=request.data.get('password')
    if not user.otp==otp:
        data={
            'success': False,
            'message': 'Incorrect OTP',
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        user.set_password(password)
        user.save()
        data={
            'success': True,
            'message': 'Password reset successfully',
            'data': get_tokens_for_user(user),
        }
        return Response(data,status=status.HTTP_200_OK)
    except Exception as e:
        data={
            'success': False,
            'message': str(e)
        }
        return Response(data,status=status.HTTP_406_NOT_ACCEPTABLE)

