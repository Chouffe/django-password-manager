from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from manager.views import CategoryDetailView
from manager.views import CategoryCreate
from manager.views import CategoryUpdate
from manager.views import CategoryDelete


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)$',
        login_required(CategoryDetailView.as_view()),
        name='details_entry'),
    url(r'^add$',
        login_required(CategoryCreate.as_view()),
        name='add_entry'),
    url(r'^update/(?P<pk>\d+)$',
        login_required(CategoryUpdate.as_view()),
        name='update_entry'),
    url(r'^delete/(?P<pk>\d+)$',
        login_required(CategoryDelete.as_view()),
        name='delete_entry'),
)
