from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from monitor.models import Host, History
from monitor import hipchat

from datetime import datetime, timedelta
import subprocess
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        lockfile = os.path.join(settings.BASE_DIR, 'cron.lock')

        try:
            if not os.path.exists(lockfile):
                time_th = datetime.now() - timedelta(minutes=4)
                hosts_to_check = Host.objects.filter(updated__lt=time_th)

                if os.name == 'posix':
                    os.mknod(lockfile)
                elif os.name == 'nt':
                    open(lockfile, 'w+').close()

                for host in hosts_to_check:
                    link = "<a href='"
                    url = "http://" + settings.ALLOWED_HOSTS[0]
                    url += reverse('monitor:detail',
                                   kwargs={'host_id': host.id})

                    link += url + "'>" + url + "</a>"

                    if os.name == 'nt':
                        proc = subprocess.Popen(['ping', '-n', '3',
                                                 host.ip4address],
                                                stdout=subprocess.PIPE)
                    elif os.name == 'posix':
                        proc = subprocess.Popen(['ping', '-c', '3',
                                                 host.ip4address],
                                                stdout=subprocess.PIPE)

                    try:
                        res = proc.communicate()
                    except:
                        pass

                    details = res[0].decode('utf-8')
                    host.status_detail = details.replace('\r\n', '<br>')
                    host.status_detail = host.status_detail.replace('\n', '<br>')

                    stat_all = History.objects.filter(host=host)
                    success = History.objects.filter(host=host, status='success')

                    stat = (len(success) / len(stat_all)) * 100

                    stat_line = "Reachable for {}% of checks in the last 24 hours".format(int(stat))


                    if '100% packet loss' in details or '100% loss' in details:
                        if host.status == 'UP':
                            host.status = 'WARNING'

                        elif host.status == 'WARNING':
                            message = "Failed to verify status of " + host.name
                            message += "<br><br>" + link
                            message += "<br><br>" + stat_line
                            host.status = 'UNREACHABLE'
                            if settings.EMAIL_NOTIFY:
                                send_mail('WARNING: ' + host.name + ' UNREACHABLE',
                                          '',
                                          settings.EMAIL_HOST_USER,
                                          settings.EMAIL_TO,
                                          html_message=message)
                            if settings.HIPCHAT_NOTIFY:
                                hipchat.send(message, 'red')


                    else:
                        host.last_seen = datetime.now()
                        if host.status == 'WARNING':
                            host.status = 'UP'
                            message = "Successfully connected to " + host.name
                            message += "<br><br>" + link
                            message += "<br><br>" + stat_line
                            if settings.EMAIL_NOTIFY:
                                send_mail('RECOVERY: ' + host.name,
                                          '',
                                          settings.EMAIL_HOST_USER,
                                          settings.EMAIL_TO,
                                          html_message=message)
                            if settings.HIPCHAT_NOTIFY:
                                hipchat.send(message, 'green')
                        elif host.status == 'UNREACHABLE':
                            host.status = 'WARNING'

                    host.save()
                    tags = {
                        'UP': 'success',
                        'WARNING': 'warning',
                        'UNREACHABLE': 'danger'
                    }
                    history = History(host=host, status=tags[host.status])
                    history.save()

                os.remove(lockfile)
                time_th = datetime.now() - timedelta(hours=24)
                History.objects.filter(stamp__lt=time_th).delete()

        except Exception as e:
            os.remove(lockfile)
            print(e)
