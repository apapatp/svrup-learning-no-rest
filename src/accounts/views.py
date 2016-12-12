from django.shortcuts import render, HttpResponseRedirect, render_to_response
from django.core.urlresolvers import reverse
from .forms import LoginForm, RegisterForm
from .models import MyUser
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def auth_login(request):
    next_url = request.GET.get('next')
    if request.POST:
        form = LoginForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_url)
    else:
        form = LoginForm()
        context = {"form": form}
    return render(request, "login.html", context)

def auth_register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password2']
        new_user = MyUser()
        new_user.username = username
        new_user.email = email
        new_user.set_password(password)
        new_user.save()

        return HttpResponseRedirect(reverse('home'))

    context = {
        "form": form,
        "action_value": "",
        "submit_btn_value": "Register"
    }
    return render(request, "accounts/register_form.html", context)

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
