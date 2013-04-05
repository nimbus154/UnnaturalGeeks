from django.http import HttpResponse
from jobtracker.models import Job, Contact, ContactForm
from django.shortcuts import redirect, render, get_object_or_404

def create(request, job_id):
# manage contact creation
    if(request.method == 'POST'):
        form = ContactForm(request.POST)
        if(form.is_valid()):
            contact = form.save(commit=False)
            contact.job_id = job_id
            contact.save()
            return redirect('/job/%s' % job_id)
        else:
            return render(request, 
                          'jobtracker/job_detail.html', 
                          {
                              'contact_form': form,
                              'job': Job.objects.get(pk=job_id),
                          })

def list(request, job_id):
    return render(request, 
                  'jobtracker/contact_list.html',
                  {
                       'job': job_id,
                  })

def detail(request, job_id, contact_id):
    return HttpResponse('details for contact %s' % contact_id)

