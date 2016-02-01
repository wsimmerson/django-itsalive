from django.conf.urls import include, url
from . import views

app_name = 'monitor'
urlpatterns = [
    url(r'^Hosts/$', views.host_list, name='host_list'),
    url(r'^Overview/$', views.overview_map, name='overview_map'),
    url(r'^Detail/(?P<host_id>[0-9]+)/$', views.detail, name='detail'),
]
