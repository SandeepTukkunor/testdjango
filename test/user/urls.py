from django.urls import path
from test.user.views import RegisterView, LoginView, PersonaldetailsView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name='login'),
    path('personal_details/', PersonaldetailsView.as_view(), name='login'),
]
