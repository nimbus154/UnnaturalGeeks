from django.http import HttpResponse
from jobtracker.models import Job, CorrespondenceForm
from django.views.generic import DetailView

class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['correspondence_form'] = CorrespondenceForm()
        return context


def index(request):
    return HttpResponse('index')
