from django.conf.urls.defaults import patterns, include, url
from . import views
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'blog/post/(?<act_id>.+)/$', views.display_post),
	url(r'blog/$', views.display_blog),
    # Examples:
    # url(r'^$', 'lavender.views.home', name='home'),
    # url(r'^lavender/', include('lavender.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)