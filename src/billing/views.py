from django.shortcuts import render
from .models import Transaction, Membership
import random
from .signals import membership_dates
from django.contrib.auth.decorators import login_required
import braintree
from django.conf import settings

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

PLAN_ID="monthly_plan"
# Create your views here.
@login_required
def account_upgrade(request):
    try:
        # something to get current customer id stored somewhere
        ObjectH.objects.get(id=something)
    except:
        # new customer result
        new_customer_result = braintree.Customer.create({
            # "first_name": "Jen",
            # "last_name": "Smith",
        })
        if new_customer_result.is_success:
            print """Customer created id = {0}""".format(new_customer_result.customer.id)
        else:
            print "Error: {0}".format(new_customer_result.message)
    trans = Transaction.objects.create_new(request.user,"aslkhjuytu7%s"%(random.randint(0,100)),25.00,"VISA")
    if trans.success:
        membership_instance, created = Membership.objects.get_or_create(user=request.user)
        # send signal to new date start
        membership_dates.send(membership_instance, new_date_start=trans.timestamp)
    return render(request, "billing/upgrade.html", {})

def billing_history(request):
    history = Transaction.objects.filter(success=True).filter(user=request.user)
    return render(request, "billing/history.html", {"queryset": history})
