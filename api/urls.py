from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required


urlpatterns = patterns(
    '',
    # url(r'^$', login_required(EntryListView.as_view()), name='details_entry'),
    url(r'^entries.json$', 'api.views.get_entries', name='api_get_entries'),
    url(r'random_key.json$', 'api.views.get_random_key', name='api_get_entries'),
    url(r'search.json$', 'api.views.get_search', name='api_get_search'),
    url(r'entry/add$', 'api.views.post_entry_add', name='api_post_entry_add'),
)
