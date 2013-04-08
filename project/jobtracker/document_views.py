from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # Django's user model

from  models import Document

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.files import File

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
            return redirect('/document/')
            
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
        
            return redirect('/document/')
