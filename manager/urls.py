from django.conf.urls.defaults import patterns, url
from manager.views import EntryDetailView, EntryCreate, EntryUpdate, EntryDelete
from manager.views import CategoryListView

urlpatterns = patterns(
    '',
    url(r'^$', CategoryListView.as_view(), name='Categories'),
    url(r'^(?P<pk>\d+)$', EntryDetailView.as_view(), name='Entry details'),
    url(r'^add$', EntryCreate.as_view(), name='entry add'),
    url(r'^update/(?P<pk>\d+)$', EntryUpdate.as_view(), name='entry update'),
    url(r'^delete/(?P<pk>\d+)$', EntryDelete.as_view(), name='entry delete'),
    url(r'^template', 'manager.views.template', name='Template'),
)
