from django.conf.urls import patterns, include, url
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import login_required
from jobtracker.models import Job
from jobtracker.views import JobDetailView
import jobtracker.contact_views
import jobtracker.correspondence_views
import jobtracker.document_views
import jobtracker.user_views

urlpatterns = patterns('jobtracker',
    url(r'^job/$', 'job_views.list'),
    url(r'^job/create$', 'job_views.create'),
    url(r'^job/edit/(?P<job_id>\d+)$', 'job_views.edit'),
    url(r'^job/(?P<pk>\d+)$', JobDetailView.as_view()),
    url(r'^job/(?P<job_id>\d+)/contact$', 'contact_views.create'),
    url(r'^job/(?P<job_id>\d+)/contact/(?P<contact_id>\d+)$', 
        'contact_views.single'),
    url(r'^job/(?P<job_id>\d+)/correspondence$', 'correspondence_views.create'),
    url(r'^job/(?P<job_id>\d+)/correspondence/(?P<correspondence_id>\d+)$',
        'correspondence_views.single'),
    url(r'^document/index/$', 'views.index'),
    url(r'^document/$', 'views.listdocs'),
    url(r'^document/(?P<doc_id>\d+)/$', 'views.getdoc'),
    url(r'^document/del/', 'views.deldoc'),
    url(r'^user$', 'user_views.register'),
    url(r'^session$', 'user_views.createSession'),
    url(r'^$', TemplateView.as_view(template_name='jobtracker/marketing.html')),
    url(r'^login/$', 'views.loginfunc'),
    url(r'^logout/$', 'views.logoutfunc'),
    url(r'^register/$', 'views.registerfunc'),
)

(r'^articles/(\d{4})/$', 'news.views.year_archive'),
