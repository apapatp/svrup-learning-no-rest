from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.urlresolvers import reverse
import urllib2
from django.conf import settings
from .utils import get_vid_for_nav_direction

# working with signals
from django.db.models.signals import pre_save, post_save

# other way to slugify fields
from django.utils.text import slugify

DEFAULT_MESSAGE = "check out maneuverbuddy"
# can create your own custom queryset if you want to as well.
class MoveQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(active=True)

        # check to make sure move has type
    def has_type(self):
        # make sure we exclude moves that only have types in them (which they should)
        return self.filter(move_type__isnull=False).exclude(move_type__exact="")

# manage all Moves query sets
class MoveManager(models.Model):
    def get_queryset(self):
        return MoveQuerySet(self.model, using=self._db)

    #creating functions that can be called and tied to the actual models
    def get_featured(self):
        # return super(MoveManager, self).filter(featured=True)
        return self.get_queryset().active().featured()

    # this will override Djangos default all query
    def all(self):
        return self.get_queryset().active().has_type().order_by('order') # to reverse, put '-order'

# Create your models here.
class Move(models.Model):
    title = models.CharField(max_length=200)
    embed_code = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1) # this will help our ordering
    tags = GenericRelation("TaggedItem", null=True, blank=True) # ussing contenttype as direct tag to allow move to choose
    share_message = models.TextField(default=DEFAULT_MESSAGE)
    featured = models.BooleanField(default=False)
    free_preview = models.BooleanField(default=False)
    move_type= models.ForeignKey("Type", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    slug = models.SlugField(default="move",null=True, blank=True, unique=True)

    objects = MoveManager() # tying this model to its video manager. So when called in
    # the view, move.objects.get_featured() will return the manager objects of the
    # featured method

    class Meta:
        """
           make slug unique this way alternatively. unique together means
           2 fields should be unique
        """
        unique_together = (('slug','move_type'),)
        ordering = ['order', '-timestamp'] # ordering here

    def __unicode__(self):
        return self.title

    def get_share_message(self):
        return urllib2.quote(self.share_message) #returns as quoted message

    # # get the next moves
    def get_next_url(self):
        move = get_vid_for_nav_direction(self, "next")
        if move is not None:
            return move.get_absolute_url()
        return None

    # get the previous moves
    def get_previous_url(self):
        move = get_vid_for_nav_direction(self, "previous")
        if move is not None:
            return move.get_absolute_url()
        return None

    #get actual link to the object
    def get_absolute_url(self):
        return reverse("move_single", kwargs={"slug": self.slug, "cat_slug": self.move_type.slug})

# class UserType(models.Model):
#     title = models.CharField(max_length=120)
#     moves = models.ManyToManyField(Move, null=True, blank=True)

def move_post_save_receiver(sender, instance, created, *args, **kwargs):
    print "arags are ", args
    print "hiiiii nothing signal sent!!!!! ", sender, " and instance type is ", instance.move_type, " created ", created
    if created:
        slug_title = slugify(instance.title)
        new_slug = "{} {}".format(instance.title, instance.id) # if there was a foreignkey that wasn't null=True, use this then instance.move_type.slug,
        try:
            obj_exists = Move.objects.get(slug=slug_title, move_type=instance.move_type)
            instance.slug = slugify(new_slug)
            instance.save()
            print "model exists, new slug generated"
        except Move.DoesNotExist:
            instance.slug = slug_title
            instance.save()
            print "slug  and mode; created"
        except Move.MultpleObjectsReturned: #exception if multiple objects are returned
            instance.slug = slugify(new_slug)
            instance.save()
            print "multiple objects returned, slug saved"
        except:
            pass

# signals using post save. On save the sender senders the model save to the function assigned
post_save.connect(move_post_save_receiver, sender=Move)


class TypeQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(active=True)

        # check to make sure move has type
    def has_type(self):
        # make sure we exclude moves that only have types in them (which they should)
        return self.filter(move_type__isnull=False).exclude(move_type__exact="")

# manage all Moves query sets
class TypeManager(models.Model):
    def get_queryset(self):
        return TypeQuerySet(self.model, using=self._db)

    #creating functions that can be called and tied to the actual models
    def get_featured(self):
        # return super(MoveManager, self).filter(featured=True)
        return self.get_queryset().active().featured()

    # this will override Djangos default all query
    def all(self):
        return self.get_queryset().active()

class Type(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, null=True, blank=True)
    tags = GenericRelation("TaggedItem", null=True, blank=True) # ussing contenttype as direct tag to allow move to choose
    image = models.FileField(upload_to='images/', null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(default="abc", unique=True)
    """
        query many to many as such models.Type.move.add(<move object>)
        many to many is used when it goes both way e.g a move can have
        many types and a type can have many moves. But its better in this
        case when a move has many types but a type only has one move.
    """
    # moves = models.ManyToManyField(Move, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    objects = TypeManager()

    #when querying a foreign key from another table, use _set in views#e.g type.move_set.all()
    # this will return all the forign keys associated with the Move from type

    class Meta:
        ordering = ['title', 'timestamp']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("type_detail", kwargs={"cat_slug": self.slug})

    def get_image_url(self):
        # for now return string but in final, return sort app first image
        # return"%s%s"%(settings.MEDIA_URL, sort.image)
        return "/images/something.jpg"

# Tag system for models
TAG_CHOICES = (
    ("python", "python"),
    ("django", "django"),
    ("home", "home"),
    ("apartment", "apartment"),
    ("muscle", "muscle"),
)
# import contenttypes
# adding fk from contenttype allows a model to effectively tie to another model class
class TaggedItem(models.Model):
    tag = models.SlugField(choices=TAG_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __unicode__(self):
        return self.tag
