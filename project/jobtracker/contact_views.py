from django.http import HttpResponse

def list(request, job_id):
    return HttpResponse('contact list for job %s' % job_id)

def detail(request, job_id, contact_id):
    return HttpResponse('details for contact %s' % contact_id)

