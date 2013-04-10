from django.http import HttpResponse
from jobtracker.models import Job, Contact, ContactForm, Correspondence
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

@login_required
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
        form = ContactForm()
    return render(request,
                    'jobtracker/contact_form.html', 
                    {'form': form, 'job_id': job_id})

@login_required
def single(request, job_id, contact_id):
    c = get_object_or_404(Contact, pk=contact_id)

    if request.method == 'POST' and '_method' in request.POST: 
        requestMethod = request.POST.get('_method', '')

        if requestMethod == 'delete':
            c.delete()
            return redirect('/job/%s' % job_id)

        elif requestMethod == 'put':
            form = ContactForm(request.POST, instance=c)
            if(form.is_valid()):
                form.save()
                return redirect('/job/%s' % job_id)
            else:
                return render(request,
                       'jobtracker/contact_edit.html',
                       { 'form': form, 'contact': c, })
    elif request.method == 'GET' and 'edit' in request.GET:
        form = ContactForm(instance=c)
        return render(request, 
                        'jobtracker/contact_edit.html', 
                        { 'form': form, 'contact': c, })
    else:
        return render(request, 
                      'jobtracker/contact_detail.html', 
                      { 'contact': c, 
                       'correspondences': Correspondence.objects.filter(contact_id=c.id), })

