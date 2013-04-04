from django.http import HttpResponse
from django.views.generic import DetailView
from jobtracker.models import Job, CorrespondenceForm
from django.shortcuts import redirect, render

class JobDetailView(DetailView):

    model = Job
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['correspondence_form'] = CorrespondenceForm()
        return context

def correspondence(request, job_id):
    if(request.method == 'POST'):
        form = CorrespondenceForm(request.POST)
        if(form.is_valid()):
            correspondence = form.save(commit=False)
            correspondence.job_id = job_id
            correspondence.save()
            return redirect('/job/%s' % job_id)
        else:
            return render(request, 'jobtracker/job_detail.html', 
                          {
                              'correspondence_form': form,
                              'job': Job.objects.get(pk=job_id),
                          })


def index(request):
    return HttpResponse('index')
