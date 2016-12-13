from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
import random
from .signals import membership_dates
import datetime

# Create your models here.
# membership
class Membership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_end = models.DateTimeField(default=timezone.now(), verbose_name="End Date")
    date_start = models.DateTimeField(default=timezone.now(), verbose_name="Start Date")

    def __unicode__(self):
        return str(self.user.email)

    def update_membership_status(self):
        if self.date_end >= timezone.now():
            self.user.is_member = True
            self.user.save()
        elif self.date_end < timezone.now():
            self.user.is_member = False
            self.user.save()
        else:
            pass

def update_account_membership_status(sender, instance, created, **kwargs):
    if not created:
        instance.update_membership_status()

post_save.connect(update_account_membership_status, sender=Membership) # since we a re using post save, the signal needs to know which model is sending the signal

# create signal to update membership
def update_membership_dates(sender, new_date_start, **kwargs):
    membership = sender
    current_date_end = membership.date_end
    if current_date_end > new_date_start:
        # append new_start date plus offset to date end of the instance
        membership.date_end = current_date_end + datetime.timedelta(days=30, hours=10) # add 30 days to the date
        membership.save()
    else:
        # set a new start date and new end date with the same offset
        membership.date_start = new_date_start
        membership.date_end = new_date_start + datetime.timedelta(days=30, hours=10) # add 30 days to the date
        membership.save()

# connect singal all to function
membership_dates.connect(update_membership_dates)

class TransactionManager(models.Manager):
    def create_new(self, user, transaction_id, amount, card_type,
    success=None, transaction_status=None, last_four=None):
        if not user:
            raise ValueError('Must be a user')
        if not transaction_id:
            raise ValueError('Must complete a transaction to add new')

        # create a new order id with random gener and some id's
        new_order_id = "%s%s%s" % (transaction_id[:2], random.randint(1,1289), transaction_id[2:])

        # create unsaved instance of the model
        new_trans = self.model(
            user=user,
            transaction_id=transaction_id,
            order_id=new_order_id,
            amount=amount,
            card_type=card_type
        )

        if success is not None:
            new_trans.success = success
            new_trans.transaction_status = transaction_status # show message if failed!

        if last_four is not None:
            new_trans.last_four = last_four

        new_trans.save(using=self._db) # save
        return new_trans

# model to handle ccard and payment transaction
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    transaction_id = models.CharField(max_length=120) # from braintree or stripe
    order_id = models.CharField(max_length=120, unique=True) # for our transaction id different from stripe or braintree
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    success = models.BooleanField(default=True)
    transaction_status=models.CharField(max_length=250, null=True, blank=True) # if fails
    card_type = models.CharField(max_length=120)
    last_four = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = TransactionManager()
    def __unicode__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']
