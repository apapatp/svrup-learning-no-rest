from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .signals import page_view
from django.utils import timezone

# tracking stuff
class PageView(models.Model):
    path = models.CharField(max_length=400)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    primary_content_type = models.ForeignKey(ContentType, related_name="notify_analytics", null=True, blank=True)
    primary_object_id = models.PositiveIntegerField(null=True, blank=True)
    primary_object = GenericForeignKey("primary_content_type", "primary_object_id") # this ties other fields together

    secondary_content_type = models.ForeignKey(ContentType, related_name="secondary_notify_analytics",
    null=True, blank=True)
    secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
    secondary_object = GenericForeignKey("secondary_content_type", "secondary_object_id") # this ties other fields together

    timestamp = models.DateTimeField(default=timezone.now())

    def __unicode__ (self):
        return self.path

def page_view_received(sender, **kwargs):
    signal = kwargs.pop('signal', None)
    page_path = kwargs.pop('page_path')
    primary_object = kwargs.pop('primary_object', None)
    secondary_object = kwargs.pop('secondary_object', None)
    user = sender
    if not user.is_authenticated(): # check whether the user is anonmymouse
        new_page_view = PageView.objects.create(path=page_path, timestamp=timezone.now())
    else:
        new_page_view = PageView.objects.create(path=page_path, user=user, timestamp=timezone.now())
    if primary_object:
        new_page_view.primary_object_id = primary_object.id
        new_page_view.primary_content_type = ContentType.objects.get_for_model(primary_object)
    if secondary_object:
        new_page_view.secondary_object_id = secondary_object.id
        new_page_view.secondary_content_type = ContentType.objects.get_for_model(secondary_object)
    # else:
    #     new_page_view, created = PageView.objects.get_or_create(path=page_path, user=user, timestamp=timezone.now())

# receiver function to handle the signsal
page_view.connect(page_view_received)
