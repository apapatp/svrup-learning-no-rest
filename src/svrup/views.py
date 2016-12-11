from django.shortcuts import render, HttpResponseRedirect
from moving.models import Move
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from accounts.forms import RegisterForm, LoginForm
from accounts.models import MyUser

@login_required() #use decorator or request.user.is_authenticated
def home(request):
    """
        check iof user is logged in
    """
    login_form = LoginForm()
    register_form = RegisterForm()
    if request.user.is_authenticated:
        name="hhhi"
        # testing our model manager
        # moves = Move.objects.get_featured()
        moves = Move.objects.all()
        embeds = []
        for move in moves:
            code = mark_safe(move.embed_code)
            embeds.append(code)
        #if not using filter in template, you can use mark_safe to make sure h
        # striong renders as html

        context = {"name": name, "moves": moves,
        "register_form": register_form,
        "login_form": login_form}
        return render(request, "home.html", context)
    else:
        return HttpResponseRedirect('/login') #some other page
