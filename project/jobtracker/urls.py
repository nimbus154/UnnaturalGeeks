from django.conf.urls import patterns, include, url
from django.views.generic import ListView, TemplateView
from jobtracker.models import Job
from jobtracker.views import JobDetailView
import jobtracker.contact_views
import jobtracker.correspondence_views
import jobtracker.document_views
import jobtracker.user_views

urlpatterns = patterns('jobtracker',
    url(r'^job$', ListView.as_view(
        model=Job,
        context_object_name='jobs')),
    url(r'^job/(?P<pk>\d+)$', JobDetailView.as_view()),
    url(r'^job/(?P<job_id>\d+)/contact$', 'contact_views.list'),
    url(r'^job/(?P<job_id>\d+)/contact/(?P<contact_id>\d+)$', 
        'contact_views.detail'),
    url(r'^job/(?P<job_id>\d+)/correspondence$', 'views.correspondence'),
    url(r'^job/(?P<job_id>\d+)/correspondence/(?P<correspondence_id>\d+)$',
        'correspondence_views.detail'),
    url(r'^document$', 'document_views.list'),
    url(r'^document/(?P<doc_id>\d+)$', 'document_views.detail'),
    url(r'^user$', 'user_views.register'),
    url(r'^session$', 'user_views.createSession'),
    url(r'^$', TemplateView.as_view(template_name='jobtracker/marketing.html')),
)
