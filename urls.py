from django.conf.urls.defaults import patterns, include, url
from manager.views import EntryDetailView

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
    url(r'^entry/(?P<pk>\d+)$', EntryDetailView.as_view(), name='Entry'),
    url(r'addentry/', 'manager.views.entry', name='entry'),
)
