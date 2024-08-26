from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Account
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


def register_user(request):
    return render(request, 'accounts/register.html')

def login_user(request):
    return render(request, 'accounts/login.html')

def seller_registration(request):
    if request.method == 'POST':
        full_name = request.POST.get('seller-name')
        email_address = request.POST.get('seller-email')
        phone_number = request.POST.get('seller-phone')
        username = request.POST.get('seller-username')
        password = request.POST.get('seller-password')
        confirm_password = request.POST.get('seller-re-password')

        errors = []

        if not full_name:
            errors.append("Full name is required!")
        if not email_address:
            errors.append("Email Address is required!")
        if not phone_number:
            errors.append("Phone number is required!")
        if not password or not confirm_password:
            errors.append("Password and confirm password are required!")
        if password != confirm_password:
            errors.append("Passwords do not match!")
        if password and len(password) < 8:
            errors.append("Password cannot be less than 8 characters!")

        if Account.objects.filter(username=username).exists():
            errors.append("Username Taken by someone!")

        if Account.objects.filter(email=email_address).exists():
            errors.append("Email Taken by someone!")

        if Account.objects.filter(phone=phone_number).exists():
            errors.append("Phone number Taken by someone!")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('seller_registration')

        user = Account.objects.create_user(
            full_name=full_name,
            email=email_address,
            phone=phone_number,
            username=username,
            is_seller=True,
            is_verified=True
        )
        user.set_password(password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return redirect('homepage')

    return render(request, 'accounts/seller_register.html')


def buyer_registration(request):
    if request.method == 'POST':
            full_name = request.POST.get('buyer-name')
            email_address = request.POST.get('buyer-email')
            phone_number = request.POST.get('buyer-phone')
            username = request.POST.get('buyer-username')
            password = request.POST.get('buyer-password')
            confirm_password = request.POST.get('buyer-re-password')

            errors = []

            if not full_name:
                errors.append("Full name is required!")
            if not email_address:
                errors.append("Email Address is required!")
            if not phone_number:
                errors.append("Phone number is required!")
            if not password or not confirm_password:
                errors.append("Password and confirm password are required!")
            if password != confirm_password:
                errors.append("Passwords do not match!")
            if password and len(password) < 8:
                errors.append("Password cannot be less than 8 characters!")

            if Account.objects.filter(username=username).exists():
                errors.append("Username Taken by someone!")

            if Account.objects.filter(email=email_address).exists():
                errors.append("Email Taken by someone!")

            if Account.objects.filter(phone=phone_number).exists():
                errors.append("Phone number Taken by someone!")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('buyer_registration')

            user = Account.objects.create_user(
                full_name=full_name,
                email=email_address,
                phone=phone_number,
                username=username,
                is_buyer=True,
                is_verified=True
            )
            user.set_password(password)
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return redirect('homepage')
        
    return render(request, 'accounts/buyer_register.html')


def seller_login(request):
    if request.method == 'POST':
        email = request.POST.get('seller-login-email')
        password = request.POST.get('seller-login-password')

        if not email and password:
            messages.error(request, 'Please enter your email or password!')
            return redirect('seller_login')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Email or password is wrong!')
            return redirect('seller_login')
        
    return render(request, 'accounts/seller_login.html')

def buyer_login(request):
    if request.method == 'POST':
        email = request.POST.get('buyer-login-email')
        password = request.POST.get('buyer-login-password')

        if not email and password:
            messages.error(request, 'Please enter your email or password!')
            return redirect('buyer_login')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Email or password is wrong!')
            return redirect('buyer_login')
        
    return render(request, 'accounts/buyer_login.html')