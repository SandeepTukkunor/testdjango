from django.urls import path
from test.user.views import RegisterView, LoginView, PersonaldetailsView, GenerateotpView, VerifyOTP

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name='login'),
    path('generate_otp/', GenerateotpView.as_view(), name = 'generate_otp_view'),
    path('verify_otp/',VerifyOTP.as_view(), name = 'verify_otp'),
    path('personal_details/', PersonaldetailsView.as_view(), name='login'),
]
