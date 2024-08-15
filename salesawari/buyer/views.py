from django.shortcuts import render


def buyer_dashboard(request):
    return render(request, 'buyer/buyer_dashboard.html')

def buyer_profile(request):
    return render(request, 'buyer/buyer_profile.html')