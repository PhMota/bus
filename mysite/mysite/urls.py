from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^bus/', include('bus.urls')),
    url(r'^admin/', admin.site.urls),
]
