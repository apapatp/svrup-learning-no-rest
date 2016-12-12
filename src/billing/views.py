from django.shortcuts import render
from .models import Transaction
import random

# Create your views here.
def account_upgrade(request):
    Transaction.objects.create_new(request.user, "aslkhjuytu7%s"%(random.randint(0,100)), 25.00, "VISA")
    return render(request, "billing/upgrade.html", {})

def billing_history(request):
    history = Transaction.objects.filter(success=True).filter(user=request.user)
    return render(request, "billing/history.html", {"queryset": history})
