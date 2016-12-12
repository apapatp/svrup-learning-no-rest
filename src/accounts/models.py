from django.db import models
# signal for when user logs in and out
from django.contrib.auth.signals import user_logged_out, user_logged_in
# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from notifications.signals import notify
# working with signals
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from billing.models import Membership

class MyUserManager(BaseUserManager):
    def create_user(self, email=None, date_of_birth=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        # if not username:
        #     raise ValueError('Raise username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# # create signal receiver function to do some kind of check when user logs in
def user_logged_in_signal(sender, signal, request, user, **kwargs):
    request.session.set_expiry(60000) # this is average session time, user gets logged out after
    membership_object, created = Membership.objects.get_or_create(user=user)
    if created:
        membership_object.date_start = timezone.now()
        membership_object.save()
        user.is_member = True
        user.save()

    # membership_object.update_membership_status()
    user.membership.update_membership_status() # we casn do this because of the 1 to 1 field

user_logged_in.connect(user_logged_in_signal)

class MyUser(AbstractBaseUser):
    # username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    is_member = models.BooleanField(default=False, verbose_name="Is Paid Member")
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        # return self.email
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.last_name
        # return self.email

    def __unicode__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser)
    bio = models.TextField(null=True, blank=True)
    facebook_link = models.CharField(max_length=320,
        null=True,
        blank=True,
        verbose_name='Facebook profile url') #if u want user profile to store this

    def __unicode__(self):
        return self.user.email

# create post receiver
def new_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        new_profile, is_created = UserProfile.objects.get_or_create(
            user=instance
        )
        print new_profile, is_created
        # create a notification to admin for new user ceation
        notify.send(
            instance,
            recipient=MyUser.objects.get(email="apapatp@gmail.com"), # admin user
            verb="New user created."
        )
# signal to connect to post_save
post_save.connect(new_user_receiver, sender=MyUser)
