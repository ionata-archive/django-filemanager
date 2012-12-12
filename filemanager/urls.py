from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('filemanager.views',
    url(r'^$', 'handler', name='filemanager'),
)
