from django.db import models


# Create your models here.
class Hostgroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Hostgroup, on_delete=models.CASCADE)
    address = models.TextField()
    ip4address = models.GenericIPAddressField()
    latitude_y = models.FloatField()
    longitude_x = models.FloatField()
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
