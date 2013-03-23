from django.http import HttpResponse

def register(request):
    return HttpResponse('create a new user')

def createSession(request):
    return HttpResponse('create a new session')
