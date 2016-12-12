from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# get media urls
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'svrup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'svrup.views.home', name="home"),
    url(r'^moves/', include('moving.urls'))
    # url(r'^moves/', include('moving.urls')),
    # url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'), # used for static tmplate
)

# if debug is true means we are local add media url to urls to serve them. Better to do this via another server
# instead of using django to also serve
if settings.DEBUG:
    urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=
    settings.MEDIA_ROOT)
    urlpatterns += patterns('',) + static(settings.STATIC_URL, document_root=
    settings.STATIC_ROOT)
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# extending url patterns to login and logout
urlpatterns += patterns('accounts.views',
    url(r'^login/', 'auth_login', name='auth_login'),
    url(r'^logout/', 'auth_logout', name='auth_logout'),
    url(r'^register/', 'auth_register', name='auth_register'),
)

# extending url patterns to comment thread
urlpatterns += patterns('comments.views',
    url(r'^comment/(?P<id>\d+)$', 'comment_thread', name="comment_thread"),
    url(r'^comment/create/$', 'comment_create_view', name="comment_create_view"),
)

# extending for the notifications view
urlpatterns += patterns('notifications.views',
    url(r'^notifications/$', 'all_notifications', name='all_notifications'),
    url(r'^notifications/getajax/$', 'get_notifications_ajax', name='get_notifications_ajax'),
    url(r'^notifications/(?P<id>\d+)/$', 'notifications_read', name="notifications_read")
)

# extending for the notifications view
urlpatterns += patterns('sort.views',
    url(r'^sorts/$', 'all_sorts', name='all_sorts'),
    url(r'^sorts/(?P<id>\d+)/$', 'sort_detail', name="sort_detail")
)
