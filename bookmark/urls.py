from django.conf.urls import url

from bookmark.views import *

urlpatterns = [
    # Class-based views for Bookmark app
    # Example: /
    url(r'^$', BookmarkLV.as_view(), name='index'),

    # Example: /99/
    url(r'^(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'),

    # Example: /add/
    url(r'^add/$', BookmarkCreateView.as_view(), name='add'),

    # Example: /change/
    url(r'^change/$', BookmarkChangeLV.as_view(), name='change'),

    # Example: /99/update/
    url(r'^(?P<pk>[0-9]+)/update/$', BookmarkUpdateView.as_view(), name='update'),

    # Example: /99/delete/
    url(r'^(?P<pk>[0-9]+)/delete/$', BookmarkDeleteView.as_view(), name="delete"),
]