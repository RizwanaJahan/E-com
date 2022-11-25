from django.shortcuts import render, redirect , reverse
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout
from .models import Product,Categories


def HomePage(request):
    return render(request, 'Main/HomePage.html')


def LOGIN(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'Username is not Found')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Username is not verified check your mail')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.success(request, 'Wrong Password')
            return redirect('/login')

        login(request, user)
        return redirect('/store')

    return render(request, 'Main/log_in.html')


def REGISTRATION(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        if User.objects.filter(username=username).first():
            messages.success(request, 'Username is Taken')
            return redirect('registration')
        elif User.objects.filter(email=email).first():
            messages.success(request, 'Email is already using')
            return redirect('registration')

        user_obj = User.objects.create(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
        profile_obj.save()
        send_mail_after_reg(email, auth_token)
        return redirect('success')

    return render(request, 'Main/registartion_page.html')


def success(request):
    return render(request, 'Main/success.html')


def token_send(request):
    return render(request, 'Main/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'OWWO,your mail is verified')
            return redirect('login')
        else:
            return redirect('error')

    except Exception as e:
        print(e)


def send_mail_after_reg(email, token):
    subject = 'Your account need to verify'
    massage = f'Hi please click the link for bring verified http://127.0.0.1:8080/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, massage, email_from, recipient_list)


def error(request):
    return render(request, 'Main/error.html')


@login_required(login_url='/')
def store(request):
    context = {}
    return render(request, 'ecom/userProfile.html', context)


def cart(request,pk):
    id = request.GET.get(id=pk)
    print(id)
    product = Product.GET.get(id = pk)
    print(product)
    Cart(product=product).save()
    return redirect('/cart')


def checkout(request):
    context = {}
    return render(request, 'ecom/Checkout.html', context)


def logout(request):
    auth_logout(request)
    return render(request, 'Main/logout.html')


def MAIN(request):
    product = Product.objects.filter(status='Publish')

    context = {
        'product': product,

    }
    return render(request, 'ecom/Main.html',context)


def PRODUCT(request,pk):
    product = Product.objects.filter(pk=pk)


    context = {
        'product': product,
    }
    return render(request, 'ecom/product.html',context)

