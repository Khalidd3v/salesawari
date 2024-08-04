from django.shortcuts import render


def buyer_dashboard(request):
    return render(request, 'buyer/dashboard.html')