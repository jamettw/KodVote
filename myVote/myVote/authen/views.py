import email

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.
def user_register(request):
    context = {}
    msg = ''
    if request.method == 'POST':
        user = User.objects.create_user(
            request.POST.get('username'),
            request.POST.get('email'),
            request.POST.get('password'),
        )
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        msg = 'ยินดีด้วย! %s คุณสมัครสมาชิกสำเร็จแล้ว' % (user.username)
    else:
        user = User.objects.none()

    context = {
        'msg': msg
    }
    return render(request, template_name='authen/register.html', context=context)

def my_login(request):
    logout(request)
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user: 
            login(request, user)
            return redirect('index')
        else:
            context['error'] = 'Username หรือ Password ไม่ถูกต้อง!'

    return render(request, template_name='authen/login.html', context=context)

def my_logout(request):
    logout(request)
    return redirect('login')
