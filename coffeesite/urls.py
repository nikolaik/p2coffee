from django.conf.urls import url, include
from django.contrib import admin

from p2coffee import urls as p2coffee_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(p2coffee_urls))
]
