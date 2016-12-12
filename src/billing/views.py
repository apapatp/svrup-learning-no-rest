from django.shortcuts import render

# Create your views here.
def account_upgrade(request):
    return render(request, "billing/upgrade.html", {})
