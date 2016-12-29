from django.shortcuts import render
from .models import Transaction, Membership, UserMerchantId
import random
from .signals import membership_dates
from django.contrib.auth.decorators import login_required
import braintree
from django.conf import settings

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                  public_key=settings.BRAINTREE_PUBLIC_KEY,
                                  private_key=settings.BRAINTREE_PRIVATE_KEY)

PLAN_ID="nnfg" # this is setup on braintree dashbioard
# Create your views here.
def billing_history(request):
    history = Transaction.objects.filter(success=True).filter(user=request.user)
    return render(request, "billing/history.html", {"queryset": history})


@login_required
def account_upgrade(request):
    # create client_token of brain tree here
    client_token = braintree.ClientToken.generate()
    try:
        # something to get current customer id stored somewhere
        merchant_object = UserMerchantId.objects.get(user=request.user)
    except UserMerchantId.DoesNotExist:
        # new customer result
        new_customer_result = braintree.Customer.create({
            # "first_name": "Jen",
            # "last_name": "Smith",
        })
        if new_customer_result.is_success:
            merchant_object = UserMerchantId.objects.create(user=request.user,customer_id=new_customer_result.customer.id)
            merchant_object.save()
            print """Customer created id = {0}""".format(new_customer_result.customer.id)
        else:
            print "Error: {0}".format(new_customer_result.message)
            # redirect somewhere
    except:
        # some other error occured
        pass

    merchant_customer_id = merchant_object.customer_id

    # get ccard stuff
    if request.method == "POST":
        print request.POST
        nonce = request.POST.get('payment_method_nonce', None)
        # update braintree about customer then get token to save to db
        if nonce is not None:
            # set a new payment method
            payment_method_result = braintree.PaymentMethod.create({
                "customer_id": merchant_customer_id,
                "payment_method_nonce": nonce,
                "options":{
                    "make_default": True
                }
            })
            the_token = payment_method_result.payment_method.token

            # create charge or subscription here
            subscription_result = braintree.Subscription.create({
                "payment_method_token": the_token,
                "plan_id": PLAN_ID
            })

            if subscription_result.is_success:
                subscription_result.subscription.transaction
                print " Woeks  "
            else:
                print subscription_result.message

            # customer_update_result = braintree.Customer.update(merchant_customer_id, {
            #     "payment_method_nonce": nonce
            # })
            # credit_card_token = customer_update_result.customer.credit_cards[0].token
            #
            # # add to subscription in braintree
            # subscription_result = braintree.Subscription.create({
            #     "payment_method_token": credit_card_token,
            #     "plan_id": PLAN_ID
            # })
            # if subscription_result:
            #     print "Works"
            #     trans_id = subscription_result.subscription.id
            #     trans = Transaction.objects.create_new(
            #     request.user,
            #     trans_id,
            #     25.00,
            #     "VISA")
            #     if trans.success:
            #         membership_instance, created = Membership.objects.get_or_create(user=request.user)
            #         # send signal to new date start
            #         membership_dates.send(membership_instance, new_date_start=trans.timestamp)
            #
            # else:
            #     print "Failes"

    context = {"client_token": client_token}
    return render(request, "billing/upgrade.html", context)
