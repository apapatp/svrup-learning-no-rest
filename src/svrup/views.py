from django.shortcuts import render, HttpResponseRedirect, render_to_response
from moving.models import Move
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from accounts.forms import RegisterForm, LoginForm
from accounts.models import MyUser
from analytics.signals import page_view

# @login_required() # use decorator or request.user.is_authenticated
def home(request):
    # send analytics signal on view
    page_view.send(request.user, page_path=request.get_full_path())
    if request.user.is_authenticated():
        context = {}
        # return HttpResponseRedirect('/dashboard')
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
        context = {
        "register_form": register_form,
        "login_form": login_form}

    return render(request, "home.html", context)
