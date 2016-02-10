from django.db import models


# Create your models here.
class Hostgroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Host(models.Model):
    geolink = "<a href='http://mygeoposition.com/'>Lookup GeoCode</a>"
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Hostgroup, on_delete=models.CASCADE)
    address = models.TextField()
    ip4address = models.GenericIPAddressField(unique=True)
    latitude_y = models.FloatField(help_text=geolink)
    longitude_x = models.FloatField(help_text=geolink)
    status = models.CharField(choices=[('UP', 'UP'),
                                       ('WARNING', 'WARNING'),
                                       ('UNREACHABLE', 'UNREACHABLE')],
                              default='WARNING',
                              max_length=11)
    status_detail = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class History(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    status = models.CharField(max_length=25)
    stamp = models.DateTimeField(auto_now=True)
