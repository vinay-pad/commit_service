from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'v1/', include('gateway_v1.urls', namespace='gateway_v1')),
]
