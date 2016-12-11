from django.shortcuts import render, Http404, HttpResponseRedirect
from .models import Move, Type, TaggedItem
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment

# Create your views here.
@login_required()
def move_single(request, cat_slug, slug):
    try:
        move_type = Type.objects.get(slug=cat_slug)
    except:
        raise Http404


    try:
        move = Move.objects.get(slug=slug)
        """
            None foreign key approach
        """
        #comments = Comment.objects.filter(comment_move=move)#
        """
            Reverse Foreign key set approach, allows use to not have to
            import the comments model, since the Comment model has
            move as a foreign key. lower model name and followed by
            _set.all(). E.g model.foreignkey_set.all()
        """
        comments = move.comment_set.all()
        # content_type = ContentType.objects.get_for_model(move) # get associated ContentType for the move instance
        # tags = TaggedItem.objects.filter(content_type=content_type, object_id=move.id)
        # print move.tags.all()
        comment_form = CommentForm()

    except Move.DoesNotExist:
        print "does not exist"
        raise Http404

    print "Move is ", move.get_share_message()
    print "Move get prev ", move.get_next_url
    # get all comments via ForeignKey
    comments = move.comment_set.all()
    c = {"move_type": move_type, "move": move, "comments": comments,
     "comment_form": comment_form}
    return render(request, "move/move_detail.html", c)

def move_list(request):
    queryset  = Move.objects.all()
    for q in queryset:
        print "This is query set ", q.get_absolute_url
        print " title ", q.title
    c = {"moves": queryset}
    return render(request, "move/move_list.html", c)

def type_list(request):
    queryset  = Type.objects.all()
    c = {"types": queryset}
    return render(request, "move/type_list.html", c)

@login_required()
def type_detail(request, cat_slug):
    try:
        move_type = Type.objects.get(slug=cat_slug)
        move = Move.objects.all()
    except:
        raise Http404

    path = request.get_full_path()
    comments = Comment.objects.filter(path=path)
    c = {"move_type": move_type, "comments": comments}
    return render(request, "move/type_detail.html", c)

# def move_single(request, id):
#     try:
#         move = Move.objects.get(id=id)
#     except Move.DoesNotExist:
#         print "does not exist"
#         raise Http404
#
#     c = {"move": move}
#     return render(request, "move/move_detail.html", c)
#
# def move_list(request):
#     queryset  = Move.objects.all()
#     c = {"moves": queryset}
#     return render(request, "move/move_list.html", c)

#
# def move_edit(request):
#     c = {}
#     return render(request, "moves/move_single.html", c)
#
# def move_create(request):
#     c = {}
#     return render(request, "moves/move_single.html", c)
