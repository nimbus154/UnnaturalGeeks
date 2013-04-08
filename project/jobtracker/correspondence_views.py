from django.http import HttpResponse
from jobtracker.models import Job, CorrespondenceForm, Correspondence, Contact
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def create(request, job_id):
# Manage correspondence creation
    job = get_object_or_404(Job, pk=job_id)
    if(request.method == 'POST'):
        form = CorrespondenceForm(request.POST, job=job)
        if(form.is_valid()):
            correspondence = form.save(commit=False)
            correspondence.job_id = job_id
            correspondence.save()
            return redirect('/job/%s' % job_id)
    else:
        form = CorrespondenceForm(job=job)
    return render(request, 
                    'jobtracker/correspondence_form.html',
                    {
                        'form': form,
                        'job_id': job_id,
                    })

@login_required
def single(request, job_id, correspondence_id):
    c = get_object_or_404(Correspondence, pk=correspondence_id)

    if(request.method == 'POST' and '_method' in request.POST): 
        requestMethod = request.POST.get('_method', '')

        if(requestMethod == 'delete'):
            c.delete()
            return redirect('/job/%s' % job_id)

        elif(requestMethod == 'put'):
            form = CorrespondenceForm(request.POST, instance=c)
            if(form.is_valid()):
                form.save()
                return redirect('/job/%s' % job_id)
    else:
        form = CorrespondenceForm(instance=c)

    return render(request, 
                    'jobtracker/correspondence_edit.html', 
                    {
                        'correspondence_form': form,
                        'correspondence': c,
                    })
