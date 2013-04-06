from django.forms.models import modelform_factory
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from jobtracker.models import Job, JobForm

@login_required
def create(request):
    JobForm = modelform_factory(Job)#, exclude=('user',))
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
	    #new_form = form.save(commit=False)
            #new_form.user = User.pk
            #new_form.save()
            return HttpResponseRedirect('/job')
    else:
        form = JobForm()
        message = "Add a job to track!"
    return render_to_response("jobtracker/job_create.html",
        {"form": form, "message": message},
        context_instance=RequestContext(request))


@login_required
def edit(request, job_id):
    j = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        f = JobForm(request.POST, instance=j)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect('/job')
    else:
        f = JobForm(instance=j)
        message = "Edit your job!"
    return render_to_response("jobtracker/job_create.html",
        {"form": f},
        context_instance=RequestContext(request))
