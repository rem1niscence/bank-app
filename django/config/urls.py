from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import core.urls
import user.urls
from user import views as user_views
from core.views import GeneratePdf, GeneratePdfHistorial

#con urlpatterns podemos mappear las urls de la pagina con sus respectivas vistas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(user.urls, namespace='user')),
    path('user/', include('django.contrib.auth.urls')),
    path('', include(core.urls, namespace='core')),
    
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        user_views.activate, name='activate'), #para el link de validacion del email

    path('pdf/consultas/', GeneratePdf.as_view(), name='get-pdf-consulta'),
    path('pdf/historial/', GeneratePdfHistorial.as_view(), name='get-pdf-historial'),
]
