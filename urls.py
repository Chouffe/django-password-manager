from django.conf.urls.defaults import patterns, include, url
from manager.views import EntryDetailView, EntryCreate, EntryUpdate, EntryDelete

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'password_manager.views.home', name='home'),
    # url(r'^password_manager/', include('password_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^entry/(?P<pk>\d+)$', EntryDetailView.as_view(), name='Entry details'),
    # url(r'addentry/', 'manager.views.entry', name='entry'),
    url(r'^entry/add$', EntryCreate.as_view(), name='entry add'),
    url(r'^entry/update/(?P<pk>\d+)$', EntryUpdate.as_view(), name='entry update'),
    url(r'^entry/delete/(?P<pk>\d+)$', EntryDelete.as_view(), name='entry delete'),
)
