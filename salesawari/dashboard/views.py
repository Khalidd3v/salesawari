from django.shortcuts import render
from accounts.custom_login_required import superuser_required

@superuser_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')