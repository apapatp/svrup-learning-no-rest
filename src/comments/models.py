from django.db import models
from accounts.models import MyUser
from moving.models import Move
from django.core.urlresolvers import reverse

class CommentManager(models.Manager):
    def all(self):
        return super(CommentManager, self).filter(active=True).filter(parent=None)

    def create_comment(self, user, text=None, path=None, comment_move=None, parent=None):
        if not user:
            raise ValueError('Must include a User, when adding a comment')

        if not comment_move:
            raise ValueError('Must include a Move, when adding a comment')

        # create the comment
        comment = self.model(
            user = user,
            text = text,
            path = path,
            comment_move = comment_move,
            parent = parent
        )
        if comment_move is not None:
            comment.comment_move = comment_move
        #add parent
        if parent is not None:
            comment.parent = parent
        comment.save(using=self._db)
        return comment

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(MyUser)
    path = models.CharField(max_length=350, null=True, blank=True)
    comment_move = models.ForeignKey(Move)
    text = models.TextField(Move, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)
    #foregign key of commnt to its self for parent/child comments
    parent = models.ForeignKey("self", null=True, blank=True, default=None)

    objects = CommentManager()

    class Meta:
        ordering = ["-timestamp"] # reverse the order

    def __unicode__(self):
        return self.user.email

    @property # this decorator will allow you to call comment.get_comment
    # instead of comment.get_comment() within the python views
    def get_comment(self):
        return self.text

    @property
    def get_origin(self):
        return self.path

    @property
    def is_child(self):
        if self.parent is not None:
            return True
        else:
            return False

    def get_children(self):
        if self.is_child:
            return None
        else:
            return Comment.objects.filter(parent=self)

    @property
    def get_absolute_url(self):
        return reverse('comment_thread', kwargs={"id": self.id})

    # get the affected users of a comment
    def get_affected_users(self):
        """
        it needs to be a parent and have children, the children, in effect, are
        affected users
        """
        comment_children = self.get_children()
        if comment_children is not None:
            users = []
            for comment in comment_children:
                if comment.user not in users:
                    users.append(comment.user)
            return users
        return None
