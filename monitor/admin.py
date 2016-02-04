from django.contrib import admin
from django.core.urlresolvers import reverse
# Register your models here.
from .models import Hostgroup, Host


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'ip4address', 'last_seen', 'updated', 'status')
    fields = ['name', 'group', 'address', 'ip4address', 'latitude_y', 'longitude_x']
    list_filter = ('group', 'status')
    search_fields = ['name', 'address', 'ip4address']

    def view_on_site(self, obj):
        return reverse('monitor:detail', kwargs={'host_id': obj.id})

admin.site.register(Host, HostAdmin)
admin.site.register(Hostgroup)
