from django.http import HttpResponse, HttpResponseRedirect
from jobtracker.models import Job, CorrespondenceForm, ContactForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['correspondence_form'] = CorrespondenceForm()
        context['contact_form'] = ContactForm()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


def index(request):
    return HttpResponse('index')

# Flavio's views

from django.shortcuts import get_object_or_404, render_to_response
#from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template import Context, loader

from  models import Document
#from jobsmodels import User
from django.contrib.auth.models import User


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
#from django.forms.fields import email_re
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



# manages all files and forms for the jobs tracking system

# Displays the available documents
@login_required
def listdocs(request):
    if request.method == 'GET':
        # retrieve and display all documents
        all_docs = Document.objects.filter(user_name=request.user).order_by('doc_ul_date')
        return render_to_response('jobtracker/listdocums.html', {'all_docs': all_docs,
                                                      'username': request.user.username},
                               context_instance=RequestContext(request))

#   posting corresponds to uploading a document
    elif request.method == 'POST':

        # all fields must have been entered         
        try:
            newdoc = Document()
            newdoc.doc_descr = request.POST['doc_descr']
            newdoc.doc_type  = request.POST['doc_type']
            newdoc.the_doc   = request.FILES['the_doc']
            newdoc.doc_mime  = request.FILES['the_doc'].content_type
  
        except :
            # display the error
            all_docs = Document.objects.filter(user_name=request.user).order_by('doc_ul_date')
            return render_to_response('jobtracker/listdocums.html', {
                'all_docs': all_docs, 'username': request.user.username,
                'error_message': "You did not enter all required data"},
                 context_instance=RequestContext(request))

        else:
            curruser = User.objects.get(username=request.user.username)
            newdoc.user_name = curruser

            newdoc.save()         

            all_docs = Document.objects.filter(user_name=request.user).order_by('doc_ul_date')
            return HttpResponseRedirect('/document/')
            
    else:       
        raise Http404


#    download (GET) or remove (DELETE) the file correcponding to
#    the document id received 
@login_required
def getdoc(request, doc_id):
    if request.method == 'GET':
        
#        this_doc = Document.objects.get(pk=1)
#        this_doc = get_object_or_404(Document, pk=doc_id)
        this_doc = get_object_or_404(Document, user_name=request.user,doc_key=doc_id)
#        this_doc =  Document.objects.filter(user_name=request.user,doc_key=doc_id)        
        # send the file as a header attachment 
        response = HttpResponse(this_doc.the_doc._get_file(), content_type= this_doc.doc_mime) #this_doc.the_doc.enctype)
        response['Content-Disposition'] = 'attachment; filename=' + this_doc.the_doc.name
        return response

@login_required
def deldoc(request):
    if request.method == 'POST':
         
        try:
        
         this_doc = get_object_or_404(Document, user_name=request.user,doc_key=request.POST['doc_id'])
         
        except :
            all_docs = Document.objects.filter(user_name=request.user).order_by('doc_ul_date')
            return render_to_response('jobtracker/listdocums.html', {
                'all_docs': all_docs, 'username': request.user.username,
                'error_message': "Document not found"},
                 context_instance=RequestContext(request))
        else:
            this_doc.the_doc.delete() # remove file
            this_doc.delete()         # remove document
        
            return HttpResponseRedirect('/document/')



def loginfunc(request):
    if request.method == 'GET':
        # display the login form    
        return render_to_response('jobtracker/loginpage.html', 
            {'error_message': "login or register your account"},
                               context_instance=RequestContext(request))

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/document/')
        else:
            # Return an 'invalid login' error message.
            return render_to_response('jobtracker/loginpage.html', {
                'error_message': "Invalid account "},
                 context_instance=RequestContext(request))


def logoutfunc(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def registerfunc(request):
    if request.method == 'GET':
        # display the login form    
        return render_to_response('jobtracker/registerpage.html', 
            {'error_message': "enter an account and password to register"},
                               context_instance=RequestContext(request))

    elif request.method == 'POST':
#        try:
#            useremail = request.POST['useremail']
#            if is_valid_email(useremail) == False:
                # display the error
#                return render_to_response('jobtracker/registerpage.html', 
#                    {'error_message': "invalid email"},
#                               context_instance=RequestContext(request))
#        except :
        useremail = 'auser@nothere.com'  # email is optional
            
        try:
            username  = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
        except :
            # display the error
            return render_to_response('jobtracker/registerpage.html', 
                {'error_message': "user id and pw are required"},
                               context_instance=RequestContext(request))
        else:
            # validate user (must not exist)
            checkuser = User.objects.filter(username__iexact=username)
            if checkuser.exists() or not is_user_valid(username):
                return render_to_response('jobtracker/registerpage.html', 
                    {'error_message': "user already exist or invalid"},
                               context_instance=RequestContext(request))
            else:                
                 # the 2 pw must match and not be space
                if password1 <= ' '  or password1 != password2: 
                    return render_to_response('jobtracker/registerpage.html', 
                        {'error_message': "Invalid password"},
                               context_instance=RequestContext(request))
                else:
                    # register the user
                    new_user = User.objects.create_user(username, useremail, password1)
                    new_user.is_active = True
                    new_user.save()
                    # login the new user
                    new_user = authenticate(username=username, password=password1)
                    if new_user is not None:
                        login(request, new_user)
                        return HttpResponseRedirect('/login/')
                    else:
                        return render_to_response('jobtracker/registerpage.html', 
                        {'error_message': "Could not create user"},
                               context_instance=RequestContext(request))

#        if User.objects.filter(email__iexact=self.cleaned_data['email']):
#            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
#        return self.cleaned_data['email']


def is_valid_email(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False
    
def is_user_valid(username):
    if re.match(r'^[\w.@+-]+$', username) != None:
        return 1
    return 0
