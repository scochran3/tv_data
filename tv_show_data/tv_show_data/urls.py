from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler403, handler404, handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tv_data.urls')),
]

handler404 = 'tv_data.views.error'
handler500 = 'tv_data.views.error'