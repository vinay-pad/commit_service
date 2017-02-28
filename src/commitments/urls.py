from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    CommitmentList,
    CommitmentDetail,
    CommitmentReadabilityCreate,
    )

urlpatterns = format_suffix_patterns([
    url(r'^$', CommitmentList.as_view(),
        name="commitments-list"),
    url(r'^(?P<pk>[0-9]+)/$',
        CommitmentDetail.as_view(),
        name="commitments-detail"),
    url(r'^(?P<pk>[0-9]+)/readability/$',
        CommitmentReadabilityCreate.as_view(),
        name="commitmentsreadability-detail"),
])
