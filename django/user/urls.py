from django.contrib.auth.views import LogoutView, LoginView #Dejaremos que django se haga cargo de las vistas para el manejo del
#login y el logout del usuario.
from django.urls import path
from user import views

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name="login"), #LoginView.as_view() es una vista que proporciona django
    path('logout', LogoutView.as_view(), name="logout"), #LogoutView.as_view() es una vista que proporciona django
    path('register', views.registrationFormExtended, name="register"),
    path('edit', views.edit_user_info, name="edit"),
]
