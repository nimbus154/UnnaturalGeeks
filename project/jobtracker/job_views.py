from django.forms.models import modelform_factory
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from jobtracker.models import Job, JobForm

@login_required
def create(request):
    JobForm = modelform_factory(Job, exclude=('user',))
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
	    new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return HttpResponseRedirect('/job')
        else:
            message = "Invalid entries... try again!"
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
            message = "Invalid entries... try again!"
    else:
        f = JobForm(instance=j)
        message = "Edit your job!"
    return render_to_response("jobtracker/job_create.html",
        {"form": f, "message": message},
        context_instance=RequestContext(request))

@login_required
def delete(request, job_id):
    j = get_object_or_404(Job, pk=job_id)

    j.delete()
    return HttpResponseRedirect('/job')

@login_required
def list(request):

    sort_state = { 
                  'applied_on': '', 
                  'job_title': '', 
                  'company': '', 
                  'city': '', 
                  'state': '', 
                  'applied_on': '', 
                 }
    # sort jobs
    if 'sort' in request.GET:
        sort_param = request.GET['sort']
        if 'order' in request.GET and request.GET['order'] == 'dsc':
            sort_param = '-' + sort_param
        else:
           sort_state[sort_param] = '=dsc'
        jobs = Job.objects.filter(user=request.user.pk).order_by(sort_param)
    else:
        jobs = Job.objects.filter(user=request.user.pk)

    return render_to_response('jobtracker/job_list.html', 
                              {'jobs': jobs, 'sort_order': sort_state}, 
                              context_instance=RequestContext(request))


