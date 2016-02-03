from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Hostgroup, Host


# Create your views here.
@login_required
def host_list(request):
    groups = Hostgroup.objects.all().order_by('-name')
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
    group = request.GET.get('hostgroup')
    message = None
    if group:
        hosts = Host.objects.filter(group__name=group)
    else:
        hosts = Host.objects.all()

    if not hosts:
        message = "Hostgroup " + group + " not found!"
        hosts = Host.objects.all()

    up = len(Host.objects.filter(status='UP'))
    warning = len(Host.objects.filter(status='WARNING'))
    unreachable = len(Host.objects.filter(status='UNREACHABLE'))
    hostgroups = Hostgroup.objects.all()
    context = {
        'hosts': hosts,
        'hostgroups': hostgroups,
        'up': up,
        'warning': warning,
        'unreachable': unreachable,
        'first_y': hosts[0].latitude_y,
        'first_x': hosts[0].longitude_x,
        'message': message
        }
    return render(request, 'monitor/overview_map.html', context)


@login_required
def warning_list(request):
    hosts = Host.objects.filter(status='WARNING')
    return render(request, 'monitor/status_list.html', {'hosts': hosts,
                                                        'type': 'Warning'})

@login_required
def unreachable_list(request):
    hosts = Host.objects.filter(status='UNREACHABLE')
    return render(request, 'monitor/status_list.html', {'hosts': hosts,
                                                        'type': 'Unreachable'})
