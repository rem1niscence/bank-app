from django.urls.conf import path
from core import views

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('history', views.MovementHistoryView.as_view(), name='mov_history'),
    path('accounts', views.CheckAccounts.as_view(), name='check_accounts'),
    path('transaction/new', views.TransactionView.as_view(),
         name='make_transaction'),
]
