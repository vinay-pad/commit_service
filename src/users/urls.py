from rest_framework.urlpatterns import format_suffix_patterns
from users import views
from django.conf.urls import url

urlpatterns = format_suffix_patterns([
    url(r'^login/$',
        views.UserAuth.as_view()),
    ])
