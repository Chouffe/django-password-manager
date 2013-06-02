from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect


def loginView(request):

    if request.POST:

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                message = 'Disabled account'
        else:
            message = 'Invalid login'

    return render(request, 'login.html', locals())


@login_required
@user_passes_test(lambda u: u.is_superuser)
def logoutView(request):
    logout(request)
    return redirect('home')
