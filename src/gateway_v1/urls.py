from django.conf.urls import include, url

urlpatterns = [
    url(r'^commitments/', include('commitments.urls', namespace='commitments')),
    url(r'^users/', include('users.urls', namespace='users')),
]
