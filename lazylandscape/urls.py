from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'sh.get.field_', name='root'),
    url(r'^get/(?P<field>\w+)$', 'sh.get.class_', name='ls'),
    url(r'^get/(?P<field>\w+)/(?P<cls>\w+)$', 'sh.get.source_', name='source`'),
   
    url(r'^Application/(?P<cls>\w+)$', 'sh.app.exec_', {'field':'Application'}),
    url(r'^Service/(?P<cls>\w+)$', 'sh.app.exec_', {'field':'Service'}),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)
