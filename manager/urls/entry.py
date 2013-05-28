from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from manager.views import EntryDetailView, EntryCreate, EntryUpdate, EntryDelete, EntryListView


urlpatterns = patterns(
    '',
    url(r'^$', login_required(EntryListView.as_view()), name='details_entry'),
    url(r'^(?P<pk>\d+)$', login_required(EntryDetailView.as_view()), name='details_entry'),
    url(r'^add$', login_required(EntryCreate.as_view()), name='add_entry'),
    url(r'^update/(?P<pk>\d+)$', login_required(EntryUpdate.as_view()), name='update_entry'),
    url(r'^delete/(?P<pk>\d+)$', login_required(EntryDelete.as_view()), name='delete_entry'),
