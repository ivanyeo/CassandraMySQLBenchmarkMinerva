from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tagteam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'tagteam.views.index', name='index'),
    url(r'^query/', include('query.urls', namespace='query'), name='query'),
    url(r'^post/', include('post.urls'), name='post'),
    url(r'^admin/', include(admin.site.urls)),
)
