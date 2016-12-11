import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.http import HttpResponse

@login_required
# Create your views here.
def all_sorts(request):
    # notifications = Notification.objects.all() # sign default django query Manager
    sorts = Sort.objects.all() # using our custom notifiction manager class
    context = {
        "sorts": sorts
    }
    return render(request, "sorts/all.html", context)

@login_required
def sort_detail(request, id):
    try:
        next = request.GET.get('next', None)
        sort = Sort.objects.get(id=id)
    except:
        # go back to all notifications if for some reason it fails
        return HttpResponseRedirect(reverse("all_sorts") )
