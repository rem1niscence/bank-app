from django.urls.conf import path
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('history', views.MovementHistoryView.as_view(), name='mov_history'),
]
