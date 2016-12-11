from django.shortcuts import render, Http404, HttpResponseRedirect
from .models import Comment
from moving.models import Move
from.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.signals import notify

@login_required
# Create your views here.
def comment_thread(request, id):
    comment = Comment.objects.get(id=id)
    form = CommentForm()
    c = {
        "comment": comment,
        "form": form
    }
    return render(request, "comments/comment_thread.html", c)


def comment_create_view(request):
    if request.method == 'POST' and request.user.is_authenticated():
        parent_id = request.POST.get('parent_id')
        move_id = request.POST.get('move_id')
        origin_path = request.POST.get('origin_path')
        try:
            move = Move.objects.get(id=move_id)
        except:
            move = None

        parent_comment=None
        if parent_id is not None:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except:
                parent_comment = None

            if parent_comment is not None and parent_comment.comment_move is not None:
                move = parent_comment.comment_move

        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            if parent_comment is not None:
                #using forms.Form approach
                new_comment = Comment.objects.create_comment(
                    user=request.user,
                    path=parent_comment.get_origin,
                    text=comment_text,
                    comment_move=move,
                    parent=parent_comment
                )
                affected_users = parent_comment.get_affected_users()
                # print 'This is comment affected users ', parent_comment.get_affected_users()
                # send signal to notify user. The sender - request.user can be a person or object sending the message
                notify.send(
                    request.user,
                    recipient=parent_comment.user,
                    verb="replied to",
                    action=new_comment,
                    affected_users= affected_users,
                    target=parent_comment
                )
                messages.success(request, "Thank you for your response <a href='/'>Linked</a>",
                extra_tags='safe')
                return HttpResponseRedirect(parent_comment.get_absolute_url)
            else:
                new_comment = Comment.objects.create_comment(
                    user=request.user,
                    path=origin_path,
                    text=comment_text,
                    comment_move=move,
                )
                # since this is a new comment, make sure we assign the target to a new move
                # option to notify super user, since that will be only need for this here
                # for this condition if block
                notify.send(
                    request.user,
                    action=new_comment,
                    recipient=request.user,
                    verb="commented on",
                    target=new_comment.comment_move
                )
                messages.success(request, "Thank you for your comment")
                return HttpResponseRedirect(new_comment.get_absolute_url)

                #using forms.ModelForm approach
                # obj_instance = comment_form.save(commit=false)
                # obj_instance.path = rquest.get_full_path()
                # obj_instance.user = request.user
                # obj_instance.save()
                '''
                    print new_comment.text
                '''
        else:
            # send a message
            print origin_path
            # send django error messages allows application to send message to user
            messages.error(request, "There was error with comment")
            return HttpResponseRedirect(origin_path)
    else:
        raise Http404
