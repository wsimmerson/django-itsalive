from django.contrib import admin

# Register your models here.
from .models import Hostgroup, Host


admin.site.register(Hostgroup)
admin.site.register(Host)
