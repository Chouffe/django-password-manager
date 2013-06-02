from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from manager.views import CategoryCreate
from manager.views import CategoryUpdate
from manager.views import CategoryDelete


urlpatterns = patterns(
    '',
    # url(r'^(?P<pk>\d+)$',
    #     login_required(CategoryDetailView.as_view()),
    #     name='details_category'),
    url(r'^add$',
        user_passes_test(lambda u: u.is_superuser)
        (login_required(CategoryCreate.as_view())),
        name='add_category'),
    url(r'^update/(?P<pk>\d+)$',
        user_passes_test(lambda u: u.is_superuser)
        (login_required(CategoryUpdate.as_view())),
        name='update_category'),
    url(r'^delete/(?P<pk>\d+)$',
        user_passes_test(lambda u: u.is_superuser)
        (login_required(CategoryDelete.as_view())),
        name='delete_category'),
)
