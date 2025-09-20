import random
import string
from django.contrib.auth import get_user_model, login,logout
from django.core.mail import send_mail
from .models import CaptchaModel
from .forms import RegisterForm,LoginForm
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from pyexpat.errors import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
User = get_user_model()


# Create your views here.
@require_http_methods(["GET", "POST"])
def zllogin(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if remember:
                    request.session.set_expiry(0)
                return redirect('/')
        else:
            print("邮箱或者密码错误")
            form.add.error('email','邮箱或者密码错误！')
            return render(request, 'login.html',context={'form':form})




@require_http_methods(['POST', 'GET'])
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('zlauth:register'))


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": "必须传递邮箱！"})
    # 生成验证码
    captcha = "".join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("知了博客注册验证码", message=f"您的注册验证码是：{captcha}", recipient_list={email}, from_email=None)
    return JsonResponse({"code": 200, "message": "验证码发送成功！"})


def zllogout(request):
    logout(request)
    return redirect('/')