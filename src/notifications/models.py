from django.conf import settings
from django.db import models
from .signals import notify
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# notification queryset. These will have all our querysets accessed from
# the notification manager
class NotificationQuerySet(models.query.QuerySet):
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
class NotificationManager(models.Manager):
    def get_queryset(self):
        # return queryset
        return NotificationQuerySet(self.model, using=self._db)

    def all_unread(self, user):
        return self.get_queryset().get_user(user).unread()

    def all_read(self, user):
        return self.get_queryset().get_user(user).read()

    def all_for_user(self, user):
        # self.get_queryset().mark_all_unread(user)
        self.get_queryset().mark_targetless(user)
        return self.get_queryset().get_user(user)

# Create your models here.
class Notification(models.Model):
    # ACTORE making the action happen
    sender_content_type = models.ForeignKey(ContentType, related_name="notify_sender")
    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey("sender_content_type", "sender_object_id") # this ties other fields together

    # description doing
    verb = models.CharField(max_length=255) # like a phrase or verb

    #action occuring
    action_content_type = models.ForeignKey(ContentType, related_name="notify_action"
    , null=True, blank=True)
    action_object_id = models.PositiveIntegerField(null=True, blank=True)
    action_object = GenericForeignKey("action_content_type", "action_object_id")

    # target of person or where action is directed to
    target_content_type = models.ForeignKey(ContentType, related_name="notify_target",
    null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey("target_content_type", "target_object_id")

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications") # related_name = "notifications"
    #notification_type = models.ChoiceField() # create a tuple of notification types. E.g
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    read = models.BooleanField(default=False)
    objects = NotificationManager()

    def __unicode__(self):
        try:
            target_url = self.target_object.get_absolute_url()
        except:
            target_url = None
        context = {
            "sender": self.sender_object,
            "verb": self.verb,
            "action": self.action_object,
            "target": self.target_object,
            "verify_read": reverse("notifications_read", kwargs={"id": self.id}),
            "target_url": target_url,
        }

        if self.target_object:
            if self.action_object and target_url:
                return "%(sender)s %(verb)s <a href='%(verify_read)s?next=%(target_url)s'>%(target)s</a> with %(action)s" % context
            if self.action_object and not target_url:
                return "%(sender)s %(verb)s %(target)s with %(action)s" % context
            return "%(sender)s %(action)s %(target)s" % context
        return "%(sender)s %(verb)s" % context

    @property
    def get_link(self): # return link to particular notification
        try:
            target_url = self.target_object.get_absolute_url()
        except:
            target_url = reverse("all_notifications")
        context = {
            "sender": self.sender_object,
            "verb": self.verb,
            "action": self.action_object,
            "target": self.target_object,
            "verify_read": reverse("notifications_read", kwargs={"id": self.id}),
            "target_url": target_url,
        }

        if self.target_object:
            return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s %(target)s with %(action)s</a>" % context
        else:
            return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s</a>" % context

# creating signals for new notifications
def new_notification(sender, **kwargs):
    print sender
    print kwargs
    recipient = kwargs.pop("recipient", None)
    verb = kwargs.pop("verb", None)
    affected_users = kwargs.pop("affected_users", None)
    print "affect users are ", affected_users
    # new_notification_create = Notification.objects.create(
    #         recipient=recipient,
    #         action=action
    #     )
    if affected_users is not None:
        for user in affected_users:
            if user == sender:
                print "don't send to me"
                pass
            else:
                print "send to me"
                new_note = Notification(
                    recipient=user,
                    verb=verb, #
                    sender_content_type= ContentType.objects.get_for_model(sender), # get the content type since this is part of the notification model
                    sender_object_id=sender.id
                )

                #loop through the target and action attributes of a notification
                for option in {"target","action"}:
                    # obj = kwargs.pop(option, None)
                    try:
                        obj = kwargs[option]
                        if obj is not None:
                            # setattr same as new_note.action_content_type = ContentType.objects.get....
                            setattr(new_note, "%s_content_type" % option, ContentType.objects.get_for_model(obj))
                            setattr(new_note, "%s_object_id" % option, obj.id)
                    except:
                        pass

                new_note.save()
                print new_note
    else:
        new_note = Notification(
            recipient=recipient,
            verb=verb, #
            sender_content_type= ContentType.objects.get_for_model(sender), # get the content type since this is part of the notification model
            sender_object_id=sender.id
        )

        #loop through the target and action attributes of a notification
        for option in {"target","action"}:
            obj = kwargs.pop(option, None)
            if obj is not None:
                # setattr same as new_note.action_content_type = ContentType.objects.get....
                setattr(new_note, "%s_content_type" % option, ContentType.objects.get_for_model(obj))
                setattr(new_note, "%s_object_id" % option, obj.id)

        new_note.save()

# on every call from a notfy.send is connected below and then creates a new notification
notify.connect(new_notification)
