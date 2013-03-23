from django.http import HttpResponse

def list(request):
    return HttpResponse('job list')

def details(request, job_id):
    return HttpResponse('details for job id %s' % job_id)
