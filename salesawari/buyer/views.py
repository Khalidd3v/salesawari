from django.shortcuts import render
from accounts.custom_login_required import dynamic_login_required
from .custom_decorators import buyer_required

@buyer_required
@dynamic_login_required
def buyer_dashboard(request):
    return render(request, 'buyer/buyer_dashboard.html')


@buyer_required
@dynamic_login_required
def buyer_profile(request):
    return render(request, 'buyer/buyer_profile.html')