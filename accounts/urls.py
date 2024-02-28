from django.urls import path
from .views import LoginView,Register,LogoutView,verify,editProfile,change_password,change_email

app_name = 'accounts'

urlpatterns = [
    path('login/',LoginView,name='login'),
    path('register/',Register,name='register'),
    path('logout/',LogoutView, name='logout'),
    path('verify/<slug>',verify,name='verify'),
    path('editprofile/',editProfile,name='edit_profile'),
    path('change_password/',change_password,name="change_password"),
    path('change_email/',change_email,name="change_email"),
]
