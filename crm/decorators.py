from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect ('crm:dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func