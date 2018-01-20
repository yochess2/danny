from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^listings/$', views.ListingList.as_view(), name='listing-list'),
    url(r'^listings/(?P<pk>[0-9]+)/$', views.ListingDetail.as_view(), name='listing-detail'),
    url(r'^categories/$', views.CategoryList.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view(), name='category-detail'),
    url(r'^specs/$', views.SpecList.as_view(), name='spec-list'),
    url(r'^specs/(?P<pk>[0-9]+)/$', views.SpecDetail.as_view(), name='spec-detail'),
    url(r'^profile/$', views.ProfileList.as_view(), name='profile-list'),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view(), name='profile-detail'),
]
