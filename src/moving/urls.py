from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'moving.views.move_list', name="move_list"),
    url(r'^$types/', 'moving.views.type_list', name="type_list"),
    url(r'^(?P<cat_slug>[\w-]+)/$', 'moving.views.type_detail', name="type_detail"),
    url(r'^(?P<cat_slug>[\w-]+)/(?P<slug>[\w-]+)$', 'moving.views.move_single', name="move_single"),
)
