from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('listings.urls')),
    url(r'^about/', include('userprofile.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
]
