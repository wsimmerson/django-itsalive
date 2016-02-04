from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from monitor.models import Host

from datetime import datetime, timedelta
import subprocess
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        time_threshold = datetime.now() - timedelta(minutes=5)
        hosts_to_check = Host.objects.filter(updated__lt=time_threshold)

        for host in hosts_to_check:
            if os.name == 'nt':
                proc = subprocess.Popen(['ping', '-n', '4', host.ip4address],
                                        stdout=subprocess.PIPE)
            elif os.name == 'posix':
                proc = subprocess.Popen(['ping', '-c', '4', host.ip4address],
                                        stdout=subprocess.PIPE)

            try:
                res = proc.communicate()
            except:
                pass

            details = res[0].decode('utf-8')
            host.status_detail = details.replace('\r\n', '<br>')
            host.status_detail = host.status_detail.replace('\n', '<br>')

            if '100% packet loss' in details or '100% loss' in details:
                if host.status == 'UP':
                    host.status = 'WARNING'
                    message = "Failed to verify status of " + host.name
                    message += "<br><br>" + host.status_detail
                    send_mail('WARNING: ' + host.name,
                              '',
                              settings.EMAIL_HOST_USER,
                              settings.EMAIL_TO,
                              html_message=message)
                elif host.status == 'WARNING':
                    message = "Failed to verify status of " + host.name
                    message += "<br><br>" + host.status_detail
                    host.status = 'UNREACHABLE'
                    send_mail('2nd WARNING: ' + host.name + ' UNREACHABLE',
                              '',
                              settings.EMAIL_HOST_USER,
                              settings.EMAIL_TO,
                              html_message=message)
            else:
                host.last_seen = datetime.now()
                if host.status == 'WARNING' or host.status == 'UNREACHABLE':
                    host.status = 'UP'
                    message = "Successfully connected to " + host.name
                    message += "<br><br>" + host.status_detail
                    send_mail('RECOVERY: ' + host.name,
                              '',
                              settings.EMAIL_HOST_USER,
                              settings.EMAIL_TO,
                              html_message=message)

            host.save()
