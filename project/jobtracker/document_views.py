from django.http import HttpResponse

def list(request):
    return HttpResponse('document list')

def details(request, doc_id):
    return HttpResponse('document id %s' % doc_id)

