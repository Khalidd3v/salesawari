from django.shortcuts import render, redirect
from django.contrib import messages


def register_user(request):
    return render(request, 'accounts/register.html')

def seller_registration(request):
    if request.method == 'POST':
        full_name = request.POST.get('seller-full-name')
        email_address = request.POST.get('seller-email-address')
        phone_number = request.POST.get('seller-phone-number')
        password = request.POST.get('seller-password')
        confirm_password = request.POST.get('seller-confirm-password')

        required_fields = [full_name, email_address, phone_number, password, confirm_password]

        for field in required_fields:
            if not field:
                messages.error(request, f"{field} is required!")
        
    return render(request, 'accounts/seller_register.html')

def buyer_registration(request):
    if request.method == 'POST':
        full_name = request.POST.get('seller-full-name')
        email_address = request.POST.get('seller-email-address')
        phone_number = request.POST.get('seller-phone-number')
        password = request.POST.get('seller-password')
        confirm_password = request.POST.get('seller-confirm-password')

        required_fields = [full_name, email_address, phone_number, password, confirm_password]

        for field in required_fields:
            if not field:
                messages.error(request, f"{field} is required!")
        
    return render(request, 'accounts/buyer_register.html')