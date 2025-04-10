from django.urls import path
from .views import *
urlpatterns = [
    path('login/',LOGIN,name = 'login'),
    path('reg/',REG,name = 'reg'),
    path('logout/',LOGOUT,name = 'logout'),
    path('reset/',RESET_PASS,name = 'reset'),
    path('success/',success,name = 'success'),
    path('error/',error,name = 'error'),
    path('token_send /',token_send,name = 'token_send'),
    path('verify/<auth_token>/',verify,name = 'verify'),
    path('Reset_user_pass/<auth_token>/',Reset_user_pass,name = 'Reset_user_pass'),
    path('success1/',success1,name = 'success1'),
    path('user_desh/',user_desh,name = 'user_desh'),


]