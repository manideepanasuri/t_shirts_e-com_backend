
from django.urls import path
from .views import *
urlpatterns = [
    path("register/", create_user_view, name="createuser"),
    path("login/", login_view, name="login"),
    path("verify/", verification_view, name="verification"),
    path("loginotp/",login_using_otp,name="loginotp"),
    path("send-otp/",sendOtp,name="send-otp"),
    path('password-reset/',password_reset_view,name="password-reset"),
]