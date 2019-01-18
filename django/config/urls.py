from django.contrib import admin
from django.urls import path, include
import core.urls
import user.urls
from django.conf.urls import url
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('/user', )
    path('user/', include(user.urls, namespace='user')),
    path('user/', include('django.contrib.auth.urls')),
    path('', include(core.urls, namespace='core')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'), #para el link de validacion del email
]
