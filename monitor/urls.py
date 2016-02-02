from django.conf.urls import include, url
from . import views

app_name = 'monitor'
urlpatterns = [
    url(r'^Hosts/$', views.host_list, name='host_list'),
    url(r'^Overview/$', views.overview_map, name='overview_map'),
    url(r'^Detail/(?P<host_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^Warning/$', views.warning_list, name='warning_list'),
    url(r'^Unreachable/$', views.unreachable_list, name='unreachable_list')
]
