from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from manager.views import CategoryListView
from django.contrib.auth.decorators import login_required


admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^$', login_required(CategoryListView.as_view()), name='home'),
    url(r'^login/$', 'manager.views.loginView', name='login'),
    url(r'^logout/$', 'manager.views.logoutView', name='logout'),
    url(r'^template', 'manager.views.template', name='template'),
    url(r'^entry/', include('manager.urls.entry')),
    url(r'^category/', include('manager.urls.category')),

    # Examples:
    # url(r'^password_manager/', include('password_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
