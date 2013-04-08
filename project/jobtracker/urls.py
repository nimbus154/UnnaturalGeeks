from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from jobtracker.models import Job
from jobtracker import contact_views, correspondence_views, document_views, user_views, auth_views

urlpatterns = patterns('jobtracker',
    url(r'^job/$', 'job_views.list'),
    url(r'^job/create$', 'job_views.create'),
    url(r'^job/edit/(?P<job_id>\d+)$', 'job_views.edit'),
    url(r'^job/delete/(?P<job_id>\d+)$', 'job_views.delete'),
    url(r'^job/(?P<job_id>\d+)$', 'job_views.detail'),
    url(r'^job/(?P<job_id>\d+)/contact$', 'contact_views.create'),
    url(r'^job/(?P<job_id>\d+)/contact/(?P<contact_id>\d+)$', 
        'contact_views.single'),
    url(r'^job/(?P<job_id>\d+)/correspondence$', 'correspondence_views.create'),
    url(r'^job/(?P<job_id>\d+)/correspondence/(?P<correspondence_id>\d+)/$',
        'correspondence_views.single'),
    url(r'^document/$', 'document_views.listdocs'),
    url(r'^document/(?P<doc_id>\d+)/$', 'document_views.getdoc'),
    url(r'^document/del/', 'views.deldoc'),
    url(r'^$', TemplateView.as_view(template_name='jobtracker/marketing.html')),
    url(r'^login/$', 'auth_views.loginfunc'),
    url(r'^logout/$', 'auth_views.logoutfunc'),
    url(r'^register/$', 'auth_views.registerfunc'),
)

(r'^articles/(\d{4})/$', 'news.views.year_archive'),
