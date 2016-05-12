from django.conf.urls import url

from p2coffee.views import CreateLogEventView, StatsView

urlpatterns = [
    url(r'^event/log/$', CreateLogEventView.as_view(), name='create-log-event'),
    url(r'^stats/$', StatsView.as_view(), name='stats'),
]
