from django.contrib.auth.forms import AuthenticationForm
from jobtracker.models import RegistrationForm
from django.template import RequestContext

from django.shortcuts import render_to_response, render, redirect

from django.contrib.auth import authenticate, login, logout

LANDING_PAGE='/job'

def logoutfunc(request):
    # logout without POST to prevent CSRF
    if request.method == 'POST':
        logout(request)
        return redirect('/login/')

def registerfunc(request):
    # thanks to http://tea.cesaroliveira.net/archives/460
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password2()
            form.save()

            # log user in
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(LANDING_PAGE)
    else:
        form = RegistrationForm()

    return render_to_response('jobtracker/register.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/job/')
        else:
            return render_to_response('jobtracker/login.html', 
                                      { 'error_message': 'Invalid account name or password. Please try again.'},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('jobtracker/login.html', {},
                                context_instance=RequestContext(request))
