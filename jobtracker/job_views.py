from django.forms.models import modelform_factory
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from jobtracker.models import Job, JobForm, Document

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

@login_required
def listdocs(request, job_id, func="none"):
    job = get_object_or_404(Job, pk=job_id)

    if func != "none":
        doc = Document.objects.get(pk=request.POST['doc_id'])
        if func == "add":
            job.document_set.add(doc)
        elif func == "rem":
            job.document_set.remove(doc)

    # retrieve and display all documents
    user_docs = Document.objects.filter(user_name=request.user).order_by('doc_ul_date')
    job_docs = user_docs.filter(user_name=request.user, job_ids=job_id).order_by('doc_ul_date')
    other_docs = user_docs.exclude(user_name=request.user, job_ids=job_id).order_by('doc_ul_date')
    return render_to_response('jobtracker/job_docs.html', {'job': job, 'job_docs': job_docs, 'other_docs': other_docs,
                                                  'username': request.user.username},
                             context_instance=RequestContext(request))



@login_required
def detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.user.id != request.user.pk:
# change to error page
        raise Http404

    contact_id = 0
    if 'contact_filter' in request.GET and request.GET['contact_filter'] != "0":
        try:
            contact_id = int(request.GET['contact_filter'])
            correspondences = job.correspondence_set.filter(contact_id=contact_id)
        except:
            correspondences = job.correspondence_set.all()
    else:
        correspondences = job.correspondence_set.all()

    return render_to_response('jobtracker/job_detail.html',
                              {
                                  'job': job,
                                  'correspondences': correspondences,
                                  'selected': contact_id,
                              },
                              context_instance=RequestContext(request))
                                

