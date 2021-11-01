from django.urls import path
from .views import Signup, ForgetPassword, login, logout, passwordChange

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', login.as_view(), name='login'),
    path('logout/', logout.as_view(), name='logout'),
    path('password_reset/', ForgetPassword.as_view(), name='password_reset'),
    path('password_change/', passwordChange.as_view(), name='password_change'),
]