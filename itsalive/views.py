from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout, login, authenticate


def front(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('monitor:host_list'))
        else:
            return render(request, 'login.html')

    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        return redirect(reverse('monitor:host_list'))


def logout_user(request):
    logout(request)
    return redirect(reverse('front'))
