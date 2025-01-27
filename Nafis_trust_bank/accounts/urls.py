from django.urls import path
from .views import UserRegisterView,UserLoginView,UserLogoutView,UserBankAccountUpdateView,change_password
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", UserBankAccountUpdateView.as_view(), name="profile"),
    path('change-password/', change_password, name='change_password'),
    
]
