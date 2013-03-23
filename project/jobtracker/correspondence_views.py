from django.http import HttpResponse

def list(request, job_id):
    return HttpResponse('correspondence list for job %s' % job_id)

def details(request, job_id, correspondence_id):
    return HttpResponse('details for correspondence %s' % correspondence_id) 
