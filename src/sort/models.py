from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from moving.models import Move
# notification queryset. These will have all our querysets accessed from
# the notification manager
class SortQuerySet(models.query.QuerySet):
    def get_user(self, user):
        return self.filter(user=user)

    # update the ones that don't have a target_object_id in the model. target is None
    def mark_targetless(self, user):
        qs = self.unread().get_user(user)
        qs_no_target = qs.filter(target_object_id=None) # need id because you cannot filter by a GenericForeignKey (contenttype)
        if qs_no_target:
            qs_no_target.update(read=True)

    def inactive(self):
        return self.filter(active=False)

    def active(self):
        return self.filter(active=True)

    # mark the sort as complete
    def mark_as_completed(self, recipient):
        qs = self.active().get_user(recipient)
        qs.update(active=False)

    # def recent(self):
    #     return self.unread()[:5] # get the 5 most recent

# notification Manager
class SortManager(models.Manager):
    def get_queryset(self):
        # return queryset
        return SortQuerySet(self.model, using=self._db)

    def all_active(self, user):
        return self.get_queryset().get_user(user).active()

# Create your models here.
class Sort(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sort_users") # related_name = "notifications"
    move = models.ForeignKey(Move, related_name="sort_move")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    area = models.ForeignKey("SortLocation", related_name="sort_by_location", default=None)
    active = models.BooleanField(default=True)
    slug = models.SlugField(default="sort", unique=True)
    objects =  SortManager()

    def __unicode__(self):
        return self.area.name

    class Meta:
        ordering = ['area', 'timestamp']

    def get_absolute_url(self):
        return reverse("type_detail", kwargs={"cat_slug": self.slug})

LOCATION_CHOICES = (
    ("kitchen", "kitchen"),
    ("living_room", "living_room"),
    ("bath", "bath"),
    ("garage", "garage"),
    ("bed_room", "bed_room"),
    ("patio", "patio"),
)

class SortLocation(models.Model):
    name = models.CharField(max_length=255, default=LOCATION_CHOICES[0])
    # item = models.IntegerField(default=0, null=True, blank=True)
    item = models.ForeignKey("SortLocationItem", related_name="sort_location_item", default=None)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(default="room", unique=True)

    def get_image_url(self):
        # for now return string but in final, return sort app first image
        # return"%s%s"%(settings.MEDIA_URL, sort.image)
        return "/images/something.jpg"

    def get_item_count(self):
        return self.item.count()

class SortLocationItem(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(default="room", unique=True)

    def __unicode__(self):
        return self.name
