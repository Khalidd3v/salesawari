from functools import wraps
from django.shortcuts import redirect

def dynamic_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if 'seller' in request.path:
                return redirect('seller_login')
            else:
                return redirect('buyer_login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('/login/superuser/')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view