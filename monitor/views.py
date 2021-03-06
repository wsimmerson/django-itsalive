from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Hostgroup, Host, History

from collections import OrderedDict
from datetime import datetime, timedelta


# Create your views here.
@login_required
def host_list(request):
    delta = datetime.now() - timedelta(hours=1)
    groups = Hostgroup.objects.all().order_by('-name')
    down = Host.objects.filter(status='UNREACHABLE', last_seen__lt=delta).order_by('last_seen')
    host_list = OrderedDict()
    sized_list = OrderedDict()
    for group in groups:
        host_list[group.name] = Host.objects.filter(group__name=group.name).order_by('name')

    for k in sorted(host_list, key=lambda k: len(host_list[k]), reverse=True):
        sized_list[k] = host_list[k]

    up = len(Host.objects.filter(status='UP'))
    warning = len(Host.objects.filter(status='WARNING'))
    unreachable = len(Host.objects.filter(status='UNREACHABLE'))
    context = {
        'host_list': sized_list,
        'up': up,
        'warning': warning,
        'unreachable': unreachable,
        'downers': down
    }

    return render(request, 'monitor/list.html', context)


@login_required
def detail(request, host_id):
    detail = get_object_or_404(Host, id=host_id)
    history = History.objects.filter(host=detail)
    opts = detail._meta
    if not history:
        percent = 0
    else:
        percent = 100 / len(history)
    context = {
               'detail': detail,
               'opts': opts,
               'history': history,
               'percent': percent
               }
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


@login_required
def history(request):
    host_id = request.GET.get('id')
    if host_id == 'None':
        host_id = None

    if host_id is not None and host_id != '':
        print(host_id)
        history = History.objects.filter(host__id=host_id).order_by('-stamp')
    else:
        history = History.objects.all().order_by('-stamp')

    paginator = Paginator(history, 300)

    page = request.GET.get('page')
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)

    context = {
        'history': history,
        'host_id': host_id
    }

    return render(request, 'monitor/history.html', context)
