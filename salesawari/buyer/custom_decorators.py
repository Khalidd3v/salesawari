from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import logout

def buyer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_buyer:
                logout(request)
                return redirect('buyer_login')
        else:
            return redirect('buyer_login')

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
