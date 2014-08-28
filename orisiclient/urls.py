from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('orisiclient.apps.main.urls', namespace='main'))
)

urlpatterns += patterns(
    'django.views.static',
    (
        r'^static/(?P<path>.*)$',
        'serve',
        {
            'document_root': 'orisiclient/static/',
            'show_indexes': True
        }
    ))
urlpatterns += patterns(
    'django.views.static',
    (
        r'^media/(?P<path>.*)$',
        'serve',
        {
            'document_root': 'orisiclient/media/',
            'show_indexes': True
        }
    ))
