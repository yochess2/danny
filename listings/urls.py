from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='listing-index-page'),
    url(r'^listings/category/(?P<category_id>[0-9]+)/$', views.ListingList.as_view(), name='listing-list-page'),
    url(r'^listings/(?P<listing_id>[0-9]+)/$', views.ListingDetail.as_view(), name='listing-detail-page')
]
