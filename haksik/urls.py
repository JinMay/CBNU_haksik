from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # installed apps
    url(r'^haksik/', include('haksik.urls', namespace="haksik")),
]
