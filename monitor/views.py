from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Hostgroup, Host


# Create your views here.
@login_required
def host_list(request):
    groups = Hostgroup.objects.all()
    host_list = {}
    for group in groups:
        host_list[group.name] = Host.objects.filter(group__name=group.name)

    up = len(Host.objects.filter(status='UP'))
    warning = len(Host.objects.filter(status='WARNING'))
    unreachable = len(Host.objects.filter(status='UNREACHABLE'))
    context = {
        'host_list': host_list,
        'up': up,
        'warning': warning,
        'unreachable': unreachable
    }

    return render(request, 'monitor/list.html', context)


@login_required
def detail(request, host_id):
    detail = get_object_or_404(Host, id=host_id)
    print(detail)
    context = {'detail': detail}
    return render(request, 'monitor/detail.html', context)


@login_required
def overview_map(request):
    hosts = Host.objects.all()
    up = len(Host.objects.filter(status='UP'))
    warning = len(Host.objects.filter(status='WARNING'))
    unreachable = len(Host.objects.filter(status='UNREACHABLE'))
    context = {
        'hosts': hosts,
        'up': up,
        'warning': warning,
        'unreachable': unreachable
        }
    return render(request, 'monitor/overview_map.html', context)


@login_required
def warning_list(request):
    hosts = Host.objects.filter(status='WARNING')
    return render(request, 'monitor/status_list.html', {'hosts': hosts,
                                                        'type': 'Warning'})

@login_required
def unreachable_list(request):
    hosts = Host.objects.filter(status='WARNING')
    return render(request, 'monitor/status_list.html', {'hosts': hosts,
                                                        'type': 'Unreachable'})
