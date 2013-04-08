from django.contrib.auth.forms import AuthenticationForm
from jobtracker.models import RegistrationForm
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout

def logoutfunc(request):
    # logout without POST to prevent CSRF
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

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
            return redirect('/job')
    else:
        form = RegistrationForm()

    return render_to_response("jobtracker/register.html",
                              {"form": form},
                              context_instance=RequestContext(request))
