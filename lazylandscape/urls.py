from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
url(r'^$', 'sh.get.field_'),
url(r'^get/(?P<field>\w+)$', 'sh.get.class_'),
url(r'^get/(?P<field>\w+)/(?P<cls>\w+)$', 'sh.get.source_'),
#url(r'^edit/(?P<field>\w+)/(?P<cls>\w+)$', 'sh.get.edit_'),
   
    url(r'^app/(?P<cls>\w+)$', 'sh.app.exec_'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)
