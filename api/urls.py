from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    '',
    # url(r'^$', login_required(EntryListView.as_view()), name='details_entry'),
    url(r'^entries.json$', 'api.views.get_entries', name='api_get_entries'),
)
