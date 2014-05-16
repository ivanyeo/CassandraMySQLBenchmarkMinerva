from django.conf.urls import patterns, url

from query import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^processquery/$',views.processquery, name='processquery'),
    url(r'^getpost/(?P<post_id>\d+)/?$',views.getpost, name='getpost'),

    # MySQL: Athena and Zeus process query
    url(r'^apq/$',views.apq, name='apq'),
    url(r'^zpq/$',views.zpq, name='zpq'),

    # Cassandra: Garfield and Odie process query
    # We only need to connect to Garfield cause Cassandra is distributed
    # and automatically connected amongst each other
    url(r'^gopq/$',views.getpost, name='gopq'),
)

