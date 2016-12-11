from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from moving.models import Move
# notification queryset. These will have all our querysets accessed from
# the notification manager
class SortQuerySet(models.query.QuerySet):
    def get_user(self, user):
        return self.filter(recipient=user)

    # update the ones that don't have a target_object_id in the model. target is None
    def mark_targetless(self, user):
        qs = self.unread().get_user(user)
        qs_no_target = qs.filter(target_object_id=None) # need id because you cannot filter by a GenericForeignKey (contenttype)
        if qs_no_target:
            qs_no_target.update(read=True)

    def mark_all_read(self, recipient):
        qs = self.unread().get_user(recipient)
        qs.update(read=True)

    def mark_all_unread(self, recipient):
        qs = self.read().get_user(recipient)
        qs.update(read=False)

    def unread(self):
        return self.filter(read=False)

    def read(self):
        return self.filter(read=True)

    def recent(self):
        return self.unread()[:5] # get the 5 most recent

# notification Manager
class SortManager(models.Manager):
    def get_queryset(self):
        # return queryset
        return SortQuerySet(self.model, using=self._db)

    def all_unread(self, user):
        return self.get_queryset().get_user(user).unread()

    def all_read(self, user):
        return self.get_queryset().get_user(user).read()

    def all_for_user(self, user):
        # self.get_queryset().mark_all_unread(user)
        self.get_queryset().mark_targetless(user)
        return self.get_queryset().get_user(user)

# Create your models here.
class Sort(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sort_users") # related_name = "notifications"
    move = models.ForeignKey(Move, related_name="sort_move")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects =  SortManager()

    def __unicode__(self):
        return self.area_name
