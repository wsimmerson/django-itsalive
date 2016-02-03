from django.contrib import admin

# Register your models here.
from .models import Hostgroup, Host


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'ip4address', 'last_seen', 'updated', 'status')
    fields = ['name', 'group', 'address', 'ip4address', 'latitude_y', 'longitude_x']

admin.site.register(Host, HostAdmin)
admin.site.register(Hostgroup)
