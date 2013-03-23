from django.conf.urls import patterns, include, url
import jobtracker.views
import jobtracker.job_views
import jobtracker.contact_views
import jobtracker.correspondence_views
import jobtracker.document_views
import jobtracker.user_views

urlpatterns = patterns('jobtracker',
    url(r'^job$', 'job_views.list'),
    url(r'^job/(?P<job_id>\d+)$', 'job_views.details'),
    url(r'^job/(?P<job_id>\d+)/contact$', 'contact_views.list'),
    url(r'^job/(?P<job_id>\d+)/contact/(?P<contact_id>\d+)$', 
        'contact_views.details'),
    url(r'^job/(?P<job_id>\d+)/correspondence$', 'correspondence_views.list'),
    url(r'^job/(?P<job_id>\d+)/correspondence/(?P<correspondence_id>\d+)$',
        'correspondence_views.details'),
    url(r'^document$', 'document_views.list'),
    url(r'^document/(?P<doc_id>\d+)$', 'document_views.details'),
    url(r'^user$', 'user_views.register'),
    url(r'^session$', 'user_views.createSession'),
    url(r'^$', 'views.index'),
)
