from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AboutDaniel.as_view(), name='about-daniel-page'),
]
