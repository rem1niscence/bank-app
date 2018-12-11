from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('login', views.login_view, name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', views.registrationFormExtended, name="register"),
    path('edit', views.edit_user_info, name='edit')
]
