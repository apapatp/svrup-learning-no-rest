import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Notification

@login_required
# Create your views here.
def all_notifications(request):
    # notifications = Notification.objects.all() # sign default django query Manager
    notifications = Notification.objects.all_for_user(request.user) # using our custom notifiction manager class
    context = {
        "notifications": notifications
    }
    return render(request, "notifications/all.html", context)

@login_required
def notifications_read(request, id):
    try:
        next = request.GET.get('next', None)
        notification = Notification.objects.get(id=id)
        # if te current user is the recipient, mark as read
        if notification.recipient == request.user:
            notification.read = True
            notification.save()
            if next is not None:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse("all_notifications") )
        else:
            raise Http404
    except:
        # go back to all notifications if for some reason it fails
        return HttpResponseRedirect(reverse("all_notifications") )

@login_required
def get_notifications_ajax(request):
    if request.is_ajax() and request.method == 'POST':
        notifications = Notification.objects.all_for_user(request.user).recent()
        count = notifications.count()
        notes = []
        for note in notifications:
            notes.append(str(note.get_link)) # get link is model instance method to get matching
            # notification link
        # create python dictionary... notice, seprate from json object but looks similar
        python_dict = {
            "notifications": notes,
            "count": count
        }
        json_data = json.dumps(python_dict) # convert to json
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404
