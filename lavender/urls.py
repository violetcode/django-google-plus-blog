from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/$', direct_to_template, {"template": "home.html"}, name="home"),    
	url(r'^', include('lavender.violetplus.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
